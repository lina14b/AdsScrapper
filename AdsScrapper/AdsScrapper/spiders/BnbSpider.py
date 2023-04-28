import scrapy
from urllib.parse import urljoin
import datetime
import pandas as pd
import os
import sys
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
from bienImmobilier import BienImmobilier



class BnbspiderSpider(scrapy.Spider):
    name = "BnbSpider"
    allowed_domains = ["www.bnb.tn"]
    start_urls = ["https://www.bnb.tn/contract/vente/"]
    custom_settings = {        
        'DOWNLOAD_DELAY': 4, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]
    }

    def parse(self, response):       
        links = response.css('a.property-row-picture-target::attr(href)').extract()
        for link in links:
           yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
           
        next_page = response.xpath('//a[contains(@class, "next")]/@href').get()        
        if next_page:
          yield scrapy.Request(url=urljoin(response.url, next_page), callback=self.parse)
    
    def parse_details(self, response):
       code=response.css('input[name="post_id"]::attr(value)').get()
       url=response.url
       status=response.css('table td:contains("Statut") + td::text').get()
       Surface=response.css('table td:contains("Surface") + td::text').get()
       Surfacelot=response.css('table td:contains("Surface du lot") + td::text').get()
       Chambres=response.css('table td:contains("Chambres") + td::text').get()
       Sallesbain=response.css('table td:contains("Salles de bain") + td::text').get()
       text = response.css('meta[itemprop="description"]::attr(content)').get()
       price = response.css('div.property-price::text').get().strip()
       images= response.css('div.property-detail-gallery a::attr(href)').getall()
       now = datetime.datetime.now()
       ScrapedDate = now.strftime("%d-%m-%y %H:%M:%S") 
       location = response.xpath('//div[@class="property-detail-subtitle"]/div[1]/a/text()').extract_first()
       location = location.strip()
    
       row ={"url": response.url,'Code':code,"description": text,"localisation":location,
            "status":status ,'surface_totale': Surface,'surface_habitable': Surfacelot,'price': price,
            "Nb_chambre":Chambres,"Nb_SalleBain":Sallesbain,
            'image_urls': images,'ScrapedDate':ScrapedDate
            
        }
       b=BienImmobilier()
       b.extractBnb(row)
       b.noneCheck()
       b.print_maison()
    #    # define file path
    #    file_path = "C:/Users/Lina/Desktop/Bnb.csv"
    #     # check if file exists, create it if it doesn't
    #    if not os.path.exists(file_path):
    #         df.to_csv(file_path, index=False)
    #    else:
    #         # read existing file into DataFrame
    #         existing_df = pd.read_csv(file_path)
            
    #         # append new DataFrame to existing file
    #         new_df = existing_df.append(df, ignore_index=True)
    #         new_df.to_csv(file_path, index=False)
       

