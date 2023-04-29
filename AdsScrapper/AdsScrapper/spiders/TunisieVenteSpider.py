import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.settings import Settings
import re
import os
from urllib.parse import urljoin
import datetime
import sys
import csv
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
from bienImmobilier import BienImmobilier
class TunisieventespiderSpider(scrapy.Spider):
    name = "TunisieVenteSpider"
    allowed_domains = ["tunisie-vente.com"]
    start_urls = ["http://www.tunisie-vente.com/ListeOffres.asp?rech_cod_cat=1&rech_cod_rub=101&rech_cod_typ=10102&rech_cod_sou_typ=undefined&rech_cod_pay=&rech_cod_vil=undefined&rech_cod_loc=undefined&rech_prix_min=undefined&rech_prix_max=undefined&rech_surf_min=undefined&rech_surf_max=undefined&rech_order_by=undefined&rech_page_num=1"]
    base_url = "http://www.tunisie-vente.com/"  
    custom_settings = {       
        'DOWNLOAD_DELAY': 5, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ######Condition d'arret
        file_path=os.getcwd()+"/AdsScrapper/first_run.csv"
        file_path = file_path.replace('/', '\\')
        with open(file_path, 'r', newline='') as file:
         first=True
         reader = csv.reader(file)
         for row in reader:
            website, date = row
            if website=="TV":
               first=False                           
        if first:
            website = 'TV'
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            with open(file_path, 'a', newline='') as file:
             writer = csv.writer(file)
             writer.writerow([website, date])
        self.first_run = first
     ####END 

    def parse(self, response):
        
        

        links = response.css('tr td.titre a::attr(href)').getall()
        selector = response.xpath('//span[@class="lst_ann_titre_blue"]')
        #Pour next page
        value = selector.css("::text").get().strip()
        offres = int(re.search(r"\d+", value).group())
        pages = round(offres // 10) 
        base,currentpage=response.url.split('rech_page_num=')
        nextpage = int(currentpage) + 1
        next_page_url=base+'rech_page_num='+str(nextpage)
        ########################
        Url_List=[]
        if not self.first_run:
         b=BienImmobilier()
         count=0

         for link in links:
            path="http://www.tunisie-vente.com/"+link
            path=path.replace(" ","")
            
            if b.ReadbyUrl(path):
               count+=1
               continue
               #raise scrapy.exceptions.CloseSpider("some_reason")
            else:
               Url_List.append(link)
               
        else: 
           Url_List=links

        if len(Url_List)==0 or count==10:
           raise scrapy.exceptions.CloseSpider("no more links to scrap")
        #############################
        
        for link in Url_List:
         yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
        
        if nextpage<=pages:
            yield scrapy.Request(url=urljoin(response.url, next_page_url), callback=self.parse)


    def parse_details(self, response):
        sel = Selector(response)

        text = response.xpath('//p[@align="justify"]/text()').extract()
        text = ''.join(text)
        text = re.sub(r'<br\s*?>', '\n', text)
        #print(text)

        now = datetime.datetime.now()
        ScrapedDate = now.strftime("%d-%m-%Y %H:%M:%S") 
        
        url = response.meta['url']
        
        localisation = response.xpath('//tr[td/b[contains(text(), "Localisation")]]/td[2]//text()').getall()
        adresse = response.xpath('//tr[td/b/text()="Adresse"]/td[2]/text()').get()
        surface = response.xpath('//tr[td/b/text()="Surface"]/td[2]/text()').get()
        price = response.xpath('//tr[td/b/text()="Prix"]/td[2]/text()').get()
        
        table = response.xpath('//table[@id="Table3"]//tr')
        date_insertion = table.xpath('.//td/b[contains(text(), "Date Insertion")]/following-sibling::text()').get()
        date_modification = table.xpath('.//td/b[contains(text(), "Date Modification")]/following-sibling::text()').get()
        date_expiration = table.xpath('.//td/b[contains(text(), "Date Expiration")]/following-sibling::text()').get()
        image_urls = response.css('img.PhotoMin1::attr(src)').getall()
        img_src_list = []
        for link in image_urls:
           
            img_src_list.append("www.tunisie-vente.com"+link)

        match = re.search(r'(?<=cod_ann=)\d+', url)
        Code=0        
        if match:
            Code = match.group()     

        yield { 'url': url,'description': text,'localisation':localisation,
            'adresse': adresse,'surface':surface,'price': price,'date_insertion':date_insertion,'date_Modification': date_modification,
            'date_Expiration': date_expiration,'image_urls': img_src_list,'Code':Code
         }
        
        
        row = {"url": response.url,'Code':Code,"description": text,"localisation":localisation,'adresse': adresse,'surface': surface,'price': price,
            'date_insertion':date_insertion,'date_Modification': date_modification,'date_Expiration': date_expiration,
            'image_urls': img_src_list   ,"ScrapedDate":ScrapedDate             
        }
        b=BienImmobilier()
        b.extractTunisieVente(row)
        b.noneCheck()
        b.print_maison()
        b.SaveDb(b)

        # # define file path
        # file_path = "C:/Users/Lina/Desktop/TunisieVente.csv"
        # # check if file exists, create it if it doesn't
        # if not os.path.exists(file_path):
        #     df.to_csv(file_path, index=False)
        # else:
        #     # read existing file into DataFrame
        #     existing_df = pd.read_csv(file_path)
            
        #     # append new DataFrame to existing file
        #     new_df = existing_df.append(df, ignore_index=True)
        #     new_df.to_csv(file_path, index=False)


