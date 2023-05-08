import scrapy
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import re
import json
import csv
import os
from bienImmobilier import BienImmobilier
from pymongo import MongoClient

class TayaraFailsSpider(scrapy.Spider):
    name = 'TayaraFailsSpider'
    allowed_domains = ['www.tayara.tn']
    start_urls = ['https://www.tayara.tn/ads/c/Immobilier/']
#'https://www.tayara.tn/ads/c/Immobilier/k/vente/'
#https://www.tayara.tn/ads/c/Immobilier/'
    custom_settings = {
        
        'DOWNLOAD_DELAY': 4, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def __init__(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.num=0
        self.parsed=False
        self.filename = 'links.csv'
        self.count=0

    
    def parse(self, response):
        # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        # db = client["AdsScrappers"]
        # collection = db["Ads"]
        # result = collection.delete_many({"website": "tayara.tn"})
        # print(result.deleted_count, "documents deleted")
              
        # Read links from CSV file into a list
        links=[]
        with open('links.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            links = [row[0] for row in reader]
        print("\n\n",len(links)) 
        # Check each link and remove it from the list if the condition is true
        b=BienImmobilier()
        i=0
        j=0
        new_links = []
        for link in links:
            if b.ReadbyUrl(link):
                i=i+1
                print(i," exist")
                pass
            else:
                j=j+1
                new_links.append(link)
                print(j," doesnt exist")

        #updated links back to CSV file
        with open('links.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['links'])
        b=BienImmobilier()
        for link in new_links:       
         if b.ReadbyUrl(link):
                self.count+=1
                print(" exist")
                continue
         else:              
                yield scrapy.Request(link, callback=self.parse_details, meta={'url':link})             
                time.sleep(3)              
                if not self.parsed:
                  with open(self.filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([link])

                self.parsed=False
                
            


    def parse_details(self, response):
     print("\n\n\n_________________start___________________________")
     self.parsed=True
     url=response.meta['url']
     time.sleep(3)
     title = response.xpath('//title/text()').get()
     
     span=response.css('div.flex.items-center.space-x-1.mb-1 span::text').getall()
     state,date=span[0].split(",")
     adress=""
     if len(span)>2:
         if "annonce(s)" in span[1]:
          adress=span[1]
     data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())
     ad_data = data['props']['pageProps']['adDetails']
     title = ad_data['title']
    #  time.sleep(1)
     description = ad_data['description']
     phone = ad_data['phone']
     price = ad_data['price']
     images=ad_data['images']
     published_on = ad_data['publishedOn']
     date = datetime.fromisoformat(published_on.replace('Z', '+00:00'))
     location = data['props']['pageProps']['adDetails']['location']
     superficie = next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Superficie'), None)
     nombre_de_chambres = next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Chambres'), None)
     nombre_de_salle_de_bain = next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Salles de bains'), None)
     transaction= next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Type de transaction'), None)
   
     
     now = datetime.now()
     ScrapedDate = now.strftime("%d-%m-%Y %H:%M:%S")       
     url = response.meta['url']
     row = {"url": url,"description": title+" "+description,"adress":adress,
            "ville":location['delegation'] ,'state': location['governorate'],'surface': superficie,'price': price,
             "Nb_chambre":nombre_de_chambres,"Nb_SalleBain":nombre_de_salle_de_bain,
            'image_urls': images,'AddedDate':date,'ScrapedDate':ScrapedDate}
     
     if not transaction:
        transaction="**"
        
     if "Ven" in transaction or not superficie:
        print("added")
        b=BienImmobilier()
        b.extractTayara(row)
        b.noneCheck()
        b.print_maison()
        b.SaveDb(b)
     print("\n\n\n__________________END__________________________")

    def closed(self, reason):
        self.driver.quit()
    
 