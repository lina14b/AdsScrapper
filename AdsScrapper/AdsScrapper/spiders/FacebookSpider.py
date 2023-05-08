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
from bienImmobilier import BienImmobilier
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import datetime
class FacebookSpider(scrapy.Spider):
    name = 'FacebookSpider'
    allowed_domains = ['www.facebook.com']
    start_urls = ['http://www.facebook.com'
                #  'https://www.facebook.com/marketplace/111663698852329/propertyforsale'
                 ]

    custom_settings = {
        
        'DOWNLOAD_DELAY': 4, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def __init__(self):
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        #code by pythonjar, not me
        #chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Edge(options=options)
        
        self.num=0
        self.parsed=False
        self.filename = 'links.csv'
        self.count=0

    def parse(self, response):
        #open the webpage
        self.driver= webdriver.Edge('C:/Users/Lina/Desktop/AdsScrapper/AdsScrapper/AdsScrapper/AdsScrapper/msedgedriver.exe')
        self.driver.get("https://www.facebook.com/login/")

        #target username
        username = WebDriverWait( self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        password = WebDriverWait( self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
        time.sleep(10)
        #enter username and password
        username.clear()
        username.send_keys("edsoftad@gmail.com")
        password.clear()
        password.send_keys("bl#25059594")

        #target the login button and click it
        button = WebDriverWait( self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        time.sleep(5)
        self.driver.get(response.url)
        print("\n\n____________________________________-")
        if "Your Pages and profiles" in response.text:
         print("loged in ")
        else:
           print("not loged in ")
        articles=""
        i=0
        self.driver.get("https://www.facebook.com/marketplace/111663698852329/propertyforsale")
        print("\n\n____________________________________-")
        if "Log In" in response.text:
         print("not loged in ")
        else:
           print("loged in ")
        b=BienImmobilier()
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
            annonces=sel.xpath("//div[@class='listing-item-container']/a[contains(@class, 'listing-item')]")
            for annonce in annonces:
                link = annonce.xpath('@href').extract()[0]
                if link not in self.links:
                    self.links.append(link)
                    self.count+=1
                    yield scrapy.Request(link, callback=self.parse_annonce)
                time.sleep(2)
            
            
            print(matches)
            for match in matches:
                print("https://www.facebook.com/marketplace/item/"+match+"/")
                path="https://www.facebook.com/marketplace/item/"+match+"/"
                if not b.ReadbyUrl(path):
                 self.parse_annonce(path)
                else:print("skiped")
                #yield scrapy.Request(path, callback=self.parse_details, meta={'url':path})             

                time.sleep(2)
        self.driver.close() 

    def parse_annonce(self,url):
        print("\n****")
        
        self.driver.get(url)
        time.sleep(10)
        body=self.driver.page_source
        
        start = 'marketplace_listing_renderable_target":'
        index = body.index(start)
        new_text = body[index+len(start):]
        end=',"is_shipping_offered'
        indexEnd=new_text.index(end)
        code=new_text[:indexEnd]
        code=str(code)+"}"
        # print(url)
        # print("this is code",code)
        # print(len(code))
        # print(type(code))
        # # Convert the string to a dictionary
        data = json.loads(code )

        # Extract the latitude and longitude values
        latitude = data['location']['latitude']
        longitude = data['location']['longitude']

        # Print the latitude and longitude values
        # print('Latitude:', latitude)
        # print('Longitude:', longitude)
        # Initialize a geolocator object
        geolocator = Nominatim(user_agent="<your user agent>")
        # Use the geolocator to get the address of the location
        location = geolocator.reverse(f"{latitude}, {longitude}",language='fr')
        fulladress=location.address
        # Print the 
        adresses=location.address.split(",")
        # print(url)
        # print(fulladress)
        # print(adresses)
        
        ####Price
        start = '"listing_price":{"amount":"'
        index = body.index(start)
        new_text = body[index+len(start):]
        end='","currency":'
        indexEnd=new_text.index(end)
        code=new_text[:indexEnd]
        price=str(code)
        # print(url)
        # print(fulladress)
        # print(adresses)
        # print("price",price)

        ####images
        start = 'class="xu1mrb x1yyh9jt x1jx8tsq"'
        index = body.index(start)
        new_text=body[index:]
        # print(new_text)
        end='Partager'
        indexEnd=new_text.index(end)
        new_text = new_text[:indexEnd]
        images=[]
        while 'src="' in new_text:
            # print("in")
            start = 'src="'
            index = new_text.index(start)
            text = new_text[index+len(start):]
            end='"'
            indexEnd=text.index(end)
            img=text[:indexEnd]
            img=img.replace("amp;","")
            images.append(str(img))
            new_text=text
        
        

        ####Description
        start = '"redacted_description":{"text":"'
        index = body.index(start)
        new_text = body[index+len(start):]
        end='},"__isMarketplaceRealEstateListing"'
        indexEnd=new_text.index(end)
        code=new_text[:indexEnd]
        code=str(code)
        # print(code)
        pattern = r'\b[a-zA-Z]{6,}\b'
        matches = re.findall(pattern, code)
        description=" "
        if len(matches)>0:
            text = re.sub(r'[\ud800-\udbff][\udc00-\udfff]', '<?>', code)
            description = text.encode('latin1').decode('iso-8859-1')
            description= description.encode('utf-8').decode('unicode_escape')
        else:
            text = re.sub(r'\\ud[8-9a-f][0-9a-f]{2}|\\ud[a-f][0-9a-f]{3}', '', code)
            description = text.encode('utf-8').decode('unicode_escape')

           
       
        # print("_______________START_____________________________________________")
        # print(url)
        # print(fulladress)
        # print(adresses)
        # print("price",price)
        # print("DESC: ",description)
        # print(images)
        now = datetime.datetime.now()
        ScrapedDate = now.strftime("%d-%m-%Y %H:%M:%S") 

        row = {"url": url,"description": description+" ..",'address': fulladress,'location': adresses,'price': price, 
            'image_urls': images ,"ScrapedDate":ScrapedDate,"inserteddate":ScrapedDate       
        }
        b=BienImmobilier()
        b.extractFB(row)
        b.noneCheck()
        b.print_maison()
        b.SaveDb(b)
        print("_______________END_____________________________________________")

