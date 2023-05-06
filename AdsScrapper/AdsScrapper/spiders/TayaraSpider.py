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

class TayaraSpider(scrapy.Spider):
    name = 'TayaraSpider'
    allowed_domains = ['www.tayara.tn']
    start_urls = ['https://www.tayara.tn/ads/c/Immobilier/']
#'https://www.tayara.tn/ads/c/Immobilier/k/vente/'
    def __init__(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.num=0
    
    def parse(self, response):
        self.driver.get(response.url)
        
        # scroll down the page and load new content as needed
        while True:
            # scroll down the page
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2) 
            
            # get the updated response object
            response = scrapy.http.HtmlResponse(
                url=self.driver.current_url,
                body=self.driver.page_source,
                encoding='utf-8'
            )
            
            hrefs = response.css('a::attr(href)').getall()
            #print(hrefs) 
            
            i=0
            articles = response.css('article')
            # print("\n\n\n\n\n\n\n\n\n\n\n\n",len(articles),self.num,"*******************************************************")
            time.sleep(5)
            articles=articles[self.num+1:]
            
            for article in articles:
            #    print(i)
               time.sleep(2)
               print("\n\n\n\n\n\n\n\n\n\n\n\n*******************************************************")
               link = article.css('a::attr(href)').get()
               print(link)
               if '/item' in link:
                yield scrapy.Request("https://www.tayara.tn"+link, callback=self.parse_details, meta={'url': "https://www.tayara.tn"+link})
                time.sleep(2)
                i+=1
                self.num+=1 
               
            
            # break out of the loop if there are no more new content to load
            if not articles:
                break
            
            # continue scrolling and loading new content if there are still more
            # hrefs to be found
            last_href = hrefs[-1]
            self.driver.execute_script(f"window.location.hash='{last_href}'")
            time.sleep(2)


    def parse_details(self, response):
     
     url=response.meta['url']
     title = response.xpath('//title/text()').get()
     price =response.css('span.mr-1::text').get(0)
     span=response.css('div.flex.items-center.space-x-1.mb-1 span::text').getall()
     state,date=span[0].split(",")
     adress=""
     if len(span)>1:
         if "annonce(s)" in span[1]:
          adress=span[1]
     data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())
     ad_data = data['props']['pageProps']['adDetails']
     title = ad_data['title']
     description = ad_data['description']
     phone = ad_data['phone']
     price = ad_data['price']
     published_on = ad_data['publishedOn']
     date = datetime.fromisoformat(published_on.replace('Z', '+00:00'))
     location = data['props']['pageProps']['adDetails']['location']
     superficie = next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Superficie'), None)
     nombre_de_chambres = next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Chambres'), None)
     nombre_de_salle_de_bain = next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Salles de bains'), None)
     transaction= next((param['value'] for param in data['props']['pageProps']['adDetails']['adParams'] if param['label'] == 'Type de transaction'), None)
     imgUrls=[]
     img_elements = response.xpath('//img[contains(@class, "w-full h-full object-cover")]')
     for img in img_elements:
            src = img.xpath('./@src').get()
            yield {'src': src}
            imgUrls.append(src)


     print("****************************************")
     print(" 1",url) 
     print(" 2",title)
     print(" 3",price)
     print(" 4",span)
     print(" 5",state,"-",date,"-",adress)
     print(" 6",get_date_from_time_ago(date))
     print(" 7",published_on)
     print(" 8",description)
     print(" 9",date)
     print(" 10",location['delegation'])
     print(" 11",location['governorate'])
     print(" 12",f"Location: {location}")
     print(" 13",f"Superficie: {superficie}")
     print(" 14",f"Nombre de chambres: {nombre_de_chambres}")
     print(" 15",f"Nombre de salle de bain: {nombre_de_salle_de_bain}")
     print(" 16",transaction)
     print(" 17",imgUrls)


     

   

        

    def closed(self, reason):
        self.driver.quit()
    
    

def get_date_from_time_ago(time_ago_text):
    # split time ago text into number and unit parts
    number=re.findall(r'\d+', time_ago_text)
    if len(number)==0:
       number=1
    else:
       number=number[0]

    print(number,"****")
    
    # number = int(number)
    # time_ago_text=time_ago_text.lower()
    # # # calculate timedelta based on the unit
    # if 'sec' in time_ago_text:
    #     delta = timedelta(seconds=number)
    # elif 'min' in time_ago_text:
    #     delta = timedelta(minutes=number)
    # elif 'hour' in time_ago_text:
    #     delta = timedelta(hours=number)
    # elif 'day' in time_ago_text:
    #     delta = timedelta(days=number)
    # elif 'week' in time_ago_text:
    #     delta = timedelta(weeks=number)
    # elif 'month' in time_ago_text:
    #     # approximate number of days in a month
    #     days = number * 30
    #     delta = timedelta(days=days)
    # else:
    #     raise ValueError(f"Unsupported time unit: {unit}")
    
    # # get the datetime object for the time ago
    # date = datetime.now() - delta
    # return date
