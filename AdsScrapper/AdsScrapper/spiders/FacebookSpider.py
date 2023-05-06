import time
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re


class FacebookSpider(scrapy.Spider):
    name = 'FacebookSpider'
    allowed_domains = ['www.facebook.com']
    start_urls = ['https://www.facebook.com/marketplace/111663698852329/propertyforsale']

    custom_settings = {
        
        'DOWNLOAD_DELAY': 4, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def __init__(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Edge(options=options)
        self.num=0
        self.parsed=False
        self.filename = 'links.csv'
        self.count=0

    def parse(self, response):
        self.driver.get(response.url)
        articles=""
        i=0
        # b=BienImmobilier()
        while i==0:
           #########################################
            i+=1

            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2) 
            response = HtmlResponse(
                url=self.driver.current_url,
                body=self.driver.page_source,
                encoding='utf-8'
            )    
            body=self.driver.page_source
            sel = scrapy.Selector(response)
            time.sleep(10)
            print("\n\nalmost done")
            time.sleep(10)
            print(body)
            time.sleep(5)
            matches = re.findall(r'"listing":{"__typename":"GroupCommerceProductItem","id":"\s+(\s+)\s+","primary_listing_photo":', body)
            pattern = r'listing":{"__typename":"GroupCommerceProductItem","id":"\s(.*?)\s,"primary_listing_photo":'
            matches = re.findall(pattern, body)
            print(matches)
            matches=[]
            while'"listing":{"__typename":"GroupCommerceProductItem","id":' in body:
  
                start = '"listing":{"__typename":"GroupCommerceProductItem","id":"'
                index = body.index(start)
                new_text = body[index+len(start):]
                end='","primary_listing_photo'
                indexEnd=new_text.index(end)
                code=new_text[:indexEnd]
                # time.sleep(10)
                # print(new_text)
                print("\n\n_______________________________________________________")
                # print(indexEnd)
                # print(code)
                matches.append(code)
                body=new_text
            # annonces=sel.xpath("//div[@class='listing-item-container']/a[contains(@class, 'listing-item')]")
            # for annonce in annonces:
            #     link = annonce.xpath('@href').extract()[0]
            #     if link not in self.links:
            #         self.links.append(link)
            #         self.count+=1
            #         yield scrapy.Request(link, callback=self.parse_annonce)
            #  time.sleep(2)
            # if self.num==0:
            #     self.num=self.count
            # if self.count==self.num+20:
            #     break
            print(matches)
        self.driver.close() 

    def parse_annonce(self, response):
        sel=scrapy.Selector(response)
        # Rest of the code ...
