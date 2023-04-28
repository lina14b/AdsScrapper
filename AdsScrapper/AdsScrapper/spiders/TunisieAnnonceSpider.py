import scrapy
from urllib.parse import urljoin
import datetime
import pandas as pd
import os
import re
import sys
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
from bienImmobilier import BienImmobilier



class TunisieannoncespiderSpider(scrapy.Spider):
    name = "TunisieAnnonceSpider"
    allowed_domains = ["www.tunisie-annonce.com"]
    start_urls = ["http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_page_num=1&rech_cod_cat=1&rech_cod_rub=101&rech_cod_typ=10102&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=11"]
    custom_settings = {
        
        #'DOWNLOAD_DELAY': 4, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def parse(self, response):
                
        links = response.css("tr.Tableau1 a::attr(href)").getall()
        i=0

        for link in links:
           if "DetailsAnnonceImmobilier" in link:
             yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})

        tds = response.css('td[width="40"]')  
        fourth_td = tds[3]   
        href = fourth_td.css('a::attr(href)').get()   
        yield {'href': href}   
        next_page_url = href
       
        #print(next_page_url)
        if next_page_url:
         yield scrapy.Request(url=urljoin(response.url, next_page_url), callback=self.parse)



    def parse_details(self, response):
       
       url=response.url
       s = url
       code = s.split("=")[1]
       td = response.xpath('//td[@class="da_field_text" and @colspan="3"][1]')
       tdcontent = td.xpath('.//a/text()').extract()
       country=tdcontent[3]
       state=tdcontent[4]
       region=tdcontent[5]
       ville=tdcontent[6]            
       #element = response.xpath('//td[@class="da_field_text" and @colspan="3"]/text()').getall()
       adress=response.xpath('//td[text()="Adresse"]/following-sibling::td/text()').get()
       surface=response.xpath('//td[text()="Surface"]/following-sibling::td/text()').get()
       prix=response.xpath('//td[text()="Prix"]/following-sibling::td/text()').get()

       #text = ''.join(response.xpath('//td[text()="Texte"]/following-sibling::td//text()').getall()).strip()
       text= '\n'.join(response.xpath('//td[text()="Texte"]/following-sibling::td//text()').getall()).replace('\n\n', '\n').strip()

    
       
       dates = response.xpath('//td[@class="da_field_text"]/text()').getall()
       dateModification=dates[-1]
       dateInsertion=dates[-1]
       
       now = datetime.datetime.now()
       ScrapedDate = now.strftime("%d-%m-%y %H:%M:%S") 
       all_photos_div = response.css('#all_photos')
       img_src_list = []
       for photo_div in all_photos_div.css('div[id^="div_photo_"]'):
            img_src = photo_div.css('img::attr(src)').get()
            img_src_list.append("www.tunisie-annonce.com"+img_src)

       row = {"url": response.url,'Code':code,"description": text,"adresse":adress,"ville":ville,"region":region,
            "state":state ,'country': country,'price': prix,"surface":surface,
            "date_insertion":dateInsertion,"date_Modification":dateModification,'image_urls': img_src_list,'ScrapedDate':ScrapedDate            
        }
       
       
       b=BienImmobilier()
       b.extractTA(row)
       b.noneCheck()
       b.print_maison()
       
       



