import time
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import json
from geopy.geocoders import Nominatim
import emoji
import chardet

import unicodedata
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
            for match in matches:
                print("https://www.facebook.com/marketplace/item/"+match+"/")
                path="https://www.facebook.com/marketplace/item/"+match+"/"
                yield scrapy.Request(path, callback=self.parse_annonce, meta={'url':path})
                #yield scrapy.Request(path, callback=self.parse_details, meta={'url':path})             

                time.sleep(2)
        self.driver.close() 

    def parse_annonce(self, response):
        print("\n****")
        url=response.meta['url']
        sel=scrapy.Selector(response)
        body=response.text
        start = 'marketplace_listing_renderable_target":'
        index = body.index(start)
        new_text = body[index+len(start):]
        end=',"is_shipping_offered'
        indexEnd=new_text.index(end)
        code=new_text[:indexEnd]
        code=str(code)+"}"
        print(url)
        print("this is code",code)
        print(len(code))
        print(type(code))
        # # Convert the string to a dictionary
        data = json.loads(code )

        # Extract the latitude and longitude values
        latitude = data['location']['latitude']
        longitude = data['location']['longitude']

        # Print the latitude and longitude values
        print('Latitude:', latitude)
        print('Longitude:', longitude)
        # Initialize a geolocator object
        geolocator = Nominatim(user_agent="<your user agent>")
        # Use the geolocator to get the address of the location
        location = geolocator.reverse(f"{latitude}, {longitude}",language='fr')
        fulladress=location.address
        # Print the 
        adresses=location.address.split(",")
        print(fulladress)
        print(adresses)
        print(location)
        # assuming you have a Selector object called "sel" that contains the HTML response
        text_content = sel.xpath('//*[contains(@id, "mount_0_0_b2")]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[8]/div[2]/div/div/div/span/text()[1]').extract_first()
        print(text_content)
        ####Des
        start = '"redacted_description":{"text":"'
        index = body.index(start)
        new_text = body[index+len(start):]
        end='},"__isMarketplaceRealEstateListing"'
        indexEnd=new_text.index(end)
        code=new_text[:indexEnd]
        code=str(code)
        print(code)
       
        print("____________________________________________________________")
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        text_without_emoji = emoji_pattern.sub('', code)
        decoded_text = text_without_emoji.encode('utf-8','surrogateescape')
        decoded_text=decoded_text.decode('unicode_escape','surrogateescape')
        

        # print the cleaned text
        print(decoded_text)
        
        print(decoded_text)
        # print("****",text)

