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
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
from bienImmobilier import BienImmobilier
import csv
class TpsspiderSpider(scrapy.Spider):
    name = "TPSSpider"
    allowed_domains = ["tps-immobiliere.com"]
    start_urls = ["https://www.tps-immobiliere.com/ventes.php?page=1&filtre=date&ordre=DESC"]
    base_url = "http://tps-immobiliere.com/"
    
    custom_settings = {
        
        'DOWNLOAD_DELAY': 4, # 10 seconds delay
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
            if website=="TPS":
               first=False                           
        if first:
            website = 'TPS'
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            with open(file_path, 'a', newline='') as file:
             writer = csv.writer(file)
             writer.writerow([website, date])
        self.first_run = first
     ####END

    def parse(self, response):
        links = response.css("a.lien_interne::attr(href)").getall()
        # ########################
        Url_List=[]
        count=0
        if not self.first_run:
         b=BienImmobilier()
         

         for link in links:
            path=response.urljoin(link)
            
            if b.ReadbyUrl(path):
               count+=1
               continue
               
            else:
               Url_List.append(link)
               
        else: 
           Url_List=links

        if len(Url_List)==0 or count==16:
           raise scrapy.exceptions.CloseSpider("no more links to scrap")
        #############################
        
        for link in Url_List:
         yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
    
        next_page = response.css("a[aria-label=Next]::attr(href)").get()
      #   print(response.url)
      #   print("*********************************************")
      #   print(next_page)
        if next_page:
           
           yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
            
    def parse_details(self, response):
       
         sel = Selector(response)
         zone = response.css("div.titre_detail span#zone::text").get()
         status = response.css("div.etat_detail::text").get().strip()
         code = response.css("input[name=id]::attr(value)").get()
         text = response.css("p::text").getall()
         text = ''.join(text).strip()
         text = re.sub(r'<br\s*?>', '\n', text)
    
         characteristics = response.css("div.titre_caracteristique::text").getall()
        
         superficie_li = response.xpath('//li[contains(.,"Superficie")]')
         superficie = superficie_li.xpath('.//mark[2]/text()').get()

         superficie_construite_li = response.xpath('//li[contains(.,"Superficie construite")]')
         superficie_construite = superficie_construite_li.xpath('.//mark[2]/text()').get()

         Nb_piece_li = response.xpath('//li[contains(.,"Nombre de pièce(s)")]')
         Nb_piece = Nb_piece_li.xpath('.//mark[2]/text()').get()

         Nb_chambre_li = response.xpath('//li[contains(.,"Nombre de chambre(s)")]')
         Nb_chambre = Nb_chambre_li.xpath('.//mark[2]/text()').get()

         Nb_SalleBain_li = response.xpath('//li[contains(.,"Nombre de salle(s) de bain")]')
         Nb_SalleBain = Nb_SalleBain_li.xpath('.//mark[2]/text()').get()

         Nb_Couchage_li = response.xpath('//li[contains(.,"Nombre de couchage(s)")]')
         Nb_Couchage = Nb_Couchage_li.xpath('.//mark[2]/text()').get()
         image_urls = response.css("div.main-carousel img::attr(src)").getall()
         img_src_list = []
         for link in image_urls:
           
            img_src_list.append("www.tps-immobiliere.com/"+link)

         price = response.css('.cadre_prix_2::text').get().strip()

         now = datetime.datetime.now()
         ScrapedDate = now.strftime("%d-%m-%Y %H:%M:%S")       

         url = response.meta['url']
         

         row = {"url": response.url,'Code':code,"description": text,"characteristics":characteristics,"localisation":zone,
            "status":status ,'surface_totale': superficie,'surface_habitable': superficie_construite,'price': price,
            "Nb_piece":Nb_piece,"Nb_chambre":Nb_chambre,"Nb_SalleBain":Nb_SalleBain,"Nb_Couchage":Nb_Couchage,
            'image_urls': img_src_list,'ScrapedDate':ScrapedDate
            
        }
         b=BienImmobilier()
         b.extractTPS(row)
         b.noneCheck()
         b.print_maison()
         b.SaveDb(b)
      #   # define file path
      #    file_path = "C:/Users/Lina/Desktop/TPS.csv"
      #    # check if file exists, create it if it doesn't
      #    if not os.path.exists(file_path):
      #       df.to_csv(file_path, index=False)
      #    else:
      #       # read existing file into DataFrame
      #       existing_df = pd.read_csv(file_path)
            
      #       # append new DataFrame to existing file
      #       new_df = existing_df.append(df, ignore_index=True)
      #       new_df.to_csv(file_path, index=False)
         
        