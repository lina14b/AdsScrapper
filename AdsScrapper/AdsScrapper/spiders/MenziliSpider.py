import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin
from datetime import datetime
import re
import os
import pandas as pd

class MenzilispiderSpider(scrapy.Spider):
    name = "MenziliSpider"
    allowed_domains = ["menzili.tn"]
    start_urls = ["https://www.menzili.tn/immo/vente-immobilier-tunisie?l=1&page=1&tri=1"]
    base_url = "https://www.menzili.tn/"

    custom_settings = {
        
        'DOWNLOAD_DELAY':  4, # seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def parse(self, response):

        links = response.css('div.col-md-5.col-sm-5.col-xs-12.li-item-list-img a::attr(href)').getall()
        for link in links:
            print(link)
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
        
        next_page = response.css('ul.pagination li a.pag-item.btn.btn-default:contains(">")::attr(href)').get()
        
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_details(self, response):
        url = response.meta['url']
        code = url.split("-")[-1]
        sel = Selector(response)
        Prix=response.css('div.product-price p::text').get()
        prix=''
        if Prix:
          prix = Prix.strip()
        Addresse = response.css('div.product-title-h1 p:last-of-type::text').get().strip()
        geo_script = response.xpath('//script[contains(text(), "var geo_ville")]/text()').get()
        geo_script=geo_script.replace("var", "")
        geo_script=geo_script.replace("geo_ville", "")
        geo_script=geo_script.replace("geo_dep", "")
        geo_script=geo_script.replace("=", "")
        geo_script= geo_script.replace("15;", "")
        geo_script= geo_script.replace("zoom", "")
        geo_script= geo_script.replace('"', "")
        values = [val.strip() for val in geo_script.split(';') if val.strip()]
        geo_ville = values[0]
        geo_dep = values[1]
        Date_Insertion = response.css('time[itemprop="datePublished"]::attr(datetime)').get()
        date_obj = datetime.strptime(Date_Insertion, '%Y-%d-%m')
        formatted_date = date_obj.strftime('%d/%m/%Y')
        Description = response.css('div.block-descr p')
        Description = Description.get().replace('<br>', '')
        Chambres = response.css('div.block-over span:contains("Chambres") + strong::text').get()
        Salle_de_bain  = response.css('div.block-over span:contains("Salle de bain") + strong::text').get()
        Pieces = response.css('div.block-over span:contains("Piéces (Totale)") + strong::text').get()
        Surface_habitable  =response.css('div.block-over span:contains("Surf habitable") + strong::text').get()
        Surface  = response.css('div.block-over span:contains("Surf terrain") + strong::text').get()
        Année_Construction = response.css('div.block-over span:contains("Année construction") + strong::text').get()
        strong_tags = response.css('strong:has(i.fa.fa-check-square)')
        Equipments=[]
        for strong_tag in strong_tags:
            text = strong_tag.xpath('string()').get().strip()
            Equipments.append(text)

        image_urls = response.css('div.slider-product img::attr(src)').extract()

        now = datetime.now()
        ScrapedDate = now.strftime("%d-%m-%y %H:%M:%S") 
        
    
        df = pd.DataFrame([{"url": response.url,'Code':code,'price': prix,'Addresse':Addresse,'ville':geo_ville,'region':geo_dep,
                            'InsertedDate':formatted_date,"description": Description,"Chambres":Chambres,
            "Salle_de_bain":Salle_de_bain ,'Pieces': Pieces,'Surface_habitable': Surface_habitable,
            "Surface_terraain":Surface,"Année_Construction":Année_Construction,'Equ,ipments':Equipments,
            'image_urls': image_urls,'ScrapedDate':ScrapedDate
            
         }])
       # define file path
        file_path = "C:/Users/Lina/Desktop/Menzili.csv"
        # check if file exists, create it if it doesn't
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
        else:
            # read existing file into DataFrame
            existing_df = pd.read_csv(file_path)
            
            # append new DataFrame to existing file
            new_df = existing_df.append(df, ignore_index=True)
            new_df.to_csv(file_path, index=False)