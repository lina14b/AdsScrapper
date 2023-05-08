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

class TayaraSpider(scrapy.Spider):
    name = 'TayaraSpider'
    allowed_domains = ['www.tayara.tn']
    start_urls = ['https://www.tayara.tn/ads/c/Immobilier/']
#'https://www.tayara.tn/ads/c/Immobilier/k/vente/'
#https://www.tayara.tn/ads/c/Immobilier/'
    custom_settings = {
        
        'DOWNLOAD_DELAY': 1, # 10 seconds delay
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

        if not os.path.isfile(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Link'])
    
    def parse(self, response):
        self.driver.get(response.url)
        articles=""
        i=0
        b=BienImmobilier()
        while True:
        
       # while self.num<30:
           #########################################

            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2) 
            response = scrapy.http.HtmlResponse(
                url=self.driver.current_url,
                body=self.driver.page_source,
                encoding='utf-8'
            )
           #########################################
            hrefs = response.css('a::attr(href)').getall()
            
            
            articlesAll = response.css('article')
            
            # time.sleep(1)
            articles=articlesAll[self.num+1:]
            # for article in articles:
            #    link = article.css('a::attr(href)').get()
            #    print(i," - ","https://www.tayara.tn"+link)
            #    i+=1
            #    self.num+=1
            
            for article in articles:
               
               self.num+=1
               link = article.css('a::attr(href)').get()
               path="https://www.tayara.tn"+link
               if b.ReadbyUrl(path):
                self.count+=1
                continue
               
               else:
                print("count",self.count)              
                yield scrapy.Request(path, callback=self.parse_details, meta={'url':path})             
                time.sleep(1)
               
                print(self.parsed)
                if not self.parsed:
                 with open(self.filename, mode='a', newline='') as file:
                    
                    writer = csv.writer(file)
                    writer.writerow([path])

                self.parsed=False
                if self.count>=30:
                  raise scrapy.exceptions.CloseSpider("no more links to scrap")
            
            
            if not articles:
                break
            
            
            last_href = hrefs[-1]
            self.driver.execute_script(f"window.location.hash='{last_href}'")
            print("out",self.num)
            time.sleep(2)
            


    def parse_details(self, response):
     print("\n\n\n_________________start___________________________")
     self.parsed=True
     url=response.meta['url']
     
     title = response.xpath('//title/text()').get()
     
    #  price =response.css('span.mr-1::text').get()
    #  time.sleep(1)
     span=response.css('div.flex.items-center.space-x-1.mb-1 span::text').getall()
     state,date=span[0].split(",")
     adress=""
     if len(span)>2:
         if "annonce(s)" in span[1]:
          adress=span[1]
     data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())
     ad_data = data['props']['pageProps']['adDetails']
     title = ad_data['title']
     time.sleep(1)
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
   

    #  print("****************************************")
    #  print("1",url) #
    #  print(" 2",title)#
    #  print(" 3",price)#
    #  print(" 4",span)
    #  print(" 5",state,"-",date,"-",adress)#
    # #  print(" 6",get_date_from_time_ago(date))
    #  print(" 7",published_on)#
    #  print(" 8",description)#
    #  print(" 9",date)#
    #  print(" 10",location['delegation'])
    #  print(" 11",location['governorate'])
    #  print(" 12",f"Location: {location}")#
    #  print(" 13",f"Superficie: {superficie}")#
    #  print(" 14",f"Nombre de chambres: {nombre_de_chambres}")
    #  print(" 15",f"Nombre de salle de bain: {nombre_de_salle_de_bain}")
    #  print(" 16",transaction)
    #  print(" 17",images)
     
     now = datetime.now()
     ScrapedDate = now.strftime("%d-%m-%Y %H:%M:%S")       
     url = response.meta['url']
     row = {"url": url,"description": title+" "+description,"adress":adress,
            "ville":location['delegation'] ,'state': location['governorate'],'surface': superficie,'price': price,
             "Nb_chambre":nombre_de_chambres,"Nb_SalleBain":nombre_de_salle_de_bain,
            'image_urls': images,'AddedDate':date,'ScrapedDate':ScrapedDate}
     test=False
     if not transaction:
        transaction="**"
        if not superficie:
           test=True

        
     if "Ven" in transaction or test:
        print("added")
        b=BienImmobilier()
        b.extractTayara(row)
        b.noneCheck()
        b.print_maison()
        b.SaveDb(b)
     print("\n\n\n__________________END__________________________")



    def closed(self, reason):
        self.driver.quit()
    