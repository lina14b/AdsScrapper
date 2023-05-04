import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin
import re
import os
import pandas as pd
import datetime
import scrapy
from scrapy_splash import SplashRequest
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bienImmobilier import BienImmobilier


class RemaxspiderSpider(scrapy.Spider):
    name = "remaxSpider"
    allowed_domains = ["remax.com.tn"]
    start_urls = ["https://www.remax.com.tn/vente-appartement",
                  "https://www.remax.com.tn/vente-duplex",
                  "https://www.remax.com.tn/vente-villa",
                  "https://www.remax.com.tn/vente-immeuble-habitation",
                  "https://www.remax.com.tn/vente-terrain-habitation",
                  "https://www.remax.com.tn/vente-bureau",
                  "https://www.remax.com.tn/vente-commerce",
                  "https://www.remax.com.tn/vente-depot"]
    
    
    
    base_url = "https://www.remax.com.tn/"

    custom_settings = {
        
        'DOWNLOAD_DELAY':  4, # seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }
    


    def parse(self, response):
       
        links = response.css('div.gallery-title a::attr(href)').getall()
        print(links)
        print(response.urljoin(links[0]))
        b=BienImmobilier()
        for link in links:
         if not b.ReadbyUrl(response.urljoin(link)):
          yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
         else: 
             print("already saved")
    
    def parse_details(self, response):
        
        sel = Selector(response)
        url=response.meta['url']
        print("****************************************")
        print(url)
        

        match = re.search(r'/(\d+-\d+)$', url)

        if match:
            string = match.group(1)
            code = string.replace('-', '')
        print(code)
        key_title = response.css('div.key-title')
        title_text = key_title.css('h1::text').get().split('-')
        categorie = title_text[0].strip()
        # print(key_title)
        # print(title_text)
        # print(categorie)
        price=''

        price_div = response.css('div.key-price-div')
        if(price_div):
         price = price_div.css('a[itemprop="price"]::text').get().strip()
        address = response.css('div.key-address::text').get().strip()
        # print(price)
        # print(address)
        data_item_row = response.css('div.data-item-row')
        pieces=''
        chambres=''
        Salles_de_bain=''
        Surface=''
        surface_constructible=''
        Parking=''
        Etage=''
        Salles_deau=''
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Nombre de pièces'  in label:
                pieces = row.css('.data-item-value span::text').get()                 
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Nombre de chambres'  in label:
                chambres = row.css('.data-item-value span::text').get()
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Nombre salles de bain'  in label:
                Salles_de_bain = row.css('.data-item-value span::text').get()
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Surface Terrain'  in label or 'm²' in label:
                Surface = row.css('.data-item-value span::text').get()
                Surface = Surface +label
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Surface constructible (m²)' in label:
                surface_constructible = row.css('.data-item-value span::text').get()        
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if  'Places de parking' in label:
                Parking = row.css('.data-item-value span::text').get()
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Nombre d''étages'in label:
                Etage = row.css('.data-item-value span::text').get()
            elif 'Etage' in label:
                Etage = row.css('.data-item-value span::text').get()               
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if 'Nombre de WC' in label:
                Salles_deau  = row.css('.data-item-value span::text').get()
      
        description = response.css("#ListingFullLeft_ctl01_DescriptionDivShort.desc-short ::text").getall()
        description2 = response.css("#ListingFullLeft_ctl00_DescriptionDivShort.desc-short ::text").getall()
        description = "".join(description).replace('\n','').replace('\r','') 
        description2 = "".join(description2).replace('\n','').replace('\r','') 
        if description:
            full=description
        if description2:
            full=description2
        description=full+" ."
        Equipement = []
        for feature_item in response.css("div.features-container span.feature-item"):
            feature = feature_item.css("::text").get()
            Equipement.append(feature)
        image_urls = response.css('#Images img::attr(src)').getall()
        img_src_list = []
        for img in response.css('img.sp-thumbnail'):
            src = img.attrib['src']
            # print(src)
            yield {'src': src}
            img_src_list.append(src)        
        now = datetime.datetime.now()
        ScrapedDate = now.strftime("%d-%m-%Y %H:%M:%S") 

        row = {"url": response.url,'Code':code,"description": description+" ..",'address': address,'surface': Surface,'price': price,
            'Etage':Etage,'Salles_deau': Salles_deau,'Equipement': Equipement,
            'image_urls': img_src_list   ,"ScrapedDate":ScrapedDate,"Parking":Parking,
            'pieces': pieces   ,"chambres":chambres,'Salles_de_bain': Salles_de_bain   ,"surface_constructible":surface_constructible,'categorie':categorie               
        }
        b=BienImmobilier()
        b.extractRemax(row)
        b.noneCheck()
        b.print_maison()
        b.SaveDb(b)




