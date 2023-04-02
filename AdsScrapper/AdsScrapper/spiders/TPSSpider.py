import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.settings import Settings
import re
import os
from urllib.parse import urljoin
import datetime

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

    def parse(self, response):
        links = response.css("a.lien_interne::attr(href)").getall()
        
        

        for link in links:
         yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
         print(link)
        
        next_page = response.css("a[aria-label=Next]::attr(href)").get()
        #if next_page:
         #   yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
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


         price = response.css('.cadre_prix_2::text').get().strip()

         now = datetime.datetime.now()

         formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
         print(formatted_date)
         
         print(zone)
         print(code)
         print(status)
         print(text)
         print(characteristics)
         print(superficie)
         print(superficie_construite)
         print(Nb_piece)
         print(Nb_chambre)
         print(Nb_SalleBain)
         print(Nb_Couchage)
         print(image_urls)

         print(price)


    #     text = response.xpath('//p[@align="justify"]/text()').extract()

    #     # join the list of text fragments into a single string
    #     text = ''.join(text)
    #     text = re.sub(r'<br\s*?>', '\n', text)
         print("_____________________________")
    #     #print(text)
        
         url = response.meta['url']
      
        
    #     localisation = response.xpath('//tr[td/b[contains(text(), "Localisation")]]/td[2]//text()').getall()
    #     adresse = response.xpath('//tr[td/b/text()="Adresse"]/td[3]/text()').get()
    #     surface = response.xpath('//tr[td/b/text()="Surface"]/td[2]/text()').get()
    #     price = response.xpath('//tr[td/b/text()="Prix"]/td[2]/text()').get()
    #     # Extract table information
    #     table = response.xpath('//table[@id="Table3"]//tr')
    #     date_insertion = table.xpath('.//td/b[contains(text(), "Date Insertion")]/following-sibling::text()').get()
    #     date_modification = table.xpath('.//td/b[contains(text(), "Date Modification")]/following-sibling::text()').get()
    #     date_expiration = table.xpath('.//td/b[contains(text(), "Date Expiration")]/following-sibling::text()').get()
    #     image_urls = response.css('img.PhotoMin1::attr(src)').getall()
    #     match = re.search(r'(?<=cod_ann=)\d+', url)
    #     Code=0
    #     if match:
    #         Code = match.group()
        

    #     yield {
    #         'url': url,             
    #         'description': text,
    #         'localisation':localisation,
    #         'adresse': surface,
    #         'price': price,
    #         'date_insertion':date_insertion,
    #         'date_Modification': date_modification,
    #         'date_Expiration': date_expiration,
    #         'image_urls': image_urls,
    #         'Code':Code
    #      }
        
    #     # Save the extracted information to an Excel file
    #     df = pd.DataFrame([{
    #         "url": response.url,
    #         "description": text,
    #         "localisation":localisation,
    #         'adresse': surface,
    #         'price': price,
    #         'date_insertion':date_insertion,
    #         'date_Modification': date_modification,
    #         'date_Expiration': date_expiration,
    #         'image_urls': image_urls,
    #         'Code':Code
            
    #     }])
        

    #     # define file path
    #     file_path = "C:/Users/Lina/Desktop/AdsScrapper/AdsScrapper/TunisieVente.csv"

       

    #     # check if file exists, create it if it doesn't
    #     if not os.path.exists(file_path):
    #         df.to_csv(file_path, index=False)
    #     else:
    #         # read existing file into DataFrame
    #         existing_df = pd.read_csv(file_path)
            
    #         # append new DataFrame to existing file
    #         new_df = existing_df.append(df, ignore_index=True)
    #         new_df.to_csv(file_path, index=False)


