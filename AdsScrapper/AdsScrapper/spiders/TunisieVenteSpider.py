import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.settings import Settings
import re
import os
        
class TunisieventespiderSpider(scrapy.Spider):
    name = "TunisieVenteSpider"
    allowed_domains = ["tunisie-vente.com"]
    start_urls = ["http://www.tunisie-vente.com/ListeOffres.asp"]
    base_url = "http://www.tunisie-vente.com/"
    
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 3,  # set the maximum number of items to extract
        'DOWNLOAD_DELAY': 10, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def parse(self, response):
        # Extract the URLs of all the listings on the page
        
        links = response.css('tr td.titre a::attr(href)').getall()
        for link in links:
         yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})


    def parse_details(self, response):
        # Extract the information from the listing page
        sel = Selector(response)
        text = response.xpath('//p[@align="justify"]/text()').extract()

        # join the list of text fragments into a single string
        text = ''.join(text)
        text = re.sub(r'<br\s*?>', '\n', text)
        print("_____________________________")
        print(text)
        
        url = response.meta['url']
        
        localisation = response.xpath('//tr[td/b[contains(text(), "Localisation")]]/td[2]//text()').getall()
        adresse = response.xpath('//tr[td/b/text()="Adresse"]/td[3]/text()').get()
        surface = response.xpath('//tr[td/b/text()="Surface"]/td[2]/text()').get()
        price = response.xpath('//tr[td/b/text()="Prix"]/td[2]/text()').get()
        # Extract table information
        table = response.xpath('//table[@id="Table3"]//tr')
        date_insertion = table.xpath('.//td/b[contains(text(), "Date Insertion")]/following-sibling::text()').get()
        date_modification = table.xpath('.//td/b[contains(text(), "Date Modification")]/following-sibling::text()').get()
        date_expiration = table.xpath('.//td/b[contains(text(), "Date Expiration")]/following-sibling::text()').get()
        image_urls = response.css('img.PhotoMin1::attr(src)').getall()
        match = re.search(r'(?<=cod_ann=)\d+', url)
        Code=0
        if match:
            Code = match.group()
        

        yield {
            'url': url,             
            'description': text,
            'localisation':localisation,
            'adresse': surface,
            'price': price,
            'date_insertion':date_insertion,
            'date_Modification': date_modification,
            'date_Expiration': date_expiration,
            'image_urls': image_urls,
            'Code':Code
         }
        
        # Save the extracted information to an Excel file
        df = pd.DataFrame([{
            "url": response.url,
            "description": text,
            "localisation":localisation,
            'adresse': surface,
            'price': price,
            'date_insertion':date_insertion,
            'date_Modification': date_modification,
            'date_Expiration': date_expiration,
            'image_urls': image_urls,
            'Code':Code
            
        }])
        

        # define file path
        file_path = "C:/Users/Lina/Desktop/AdsScrapper/AdsScrapper/my_data.csv"

       

        # check if file exists, create it if it doesn't
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
        else:
            # read existing file into DataFrame
            existing_df = pd.read_csv(file_path)
            
            # append new DataFrame to existing file
            new_df = existing_df.append(df, ignore_index=True)
            new_df.to_csv(file_path, index=False)


