import scrapy
import os
import datetime
import re
import pandas as pd
import sys
import csv
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
from bienImmobilier import BienImmobilier

class TunisiapromospiderSpider(scrapy.Spider):
 
    name = "tunisiapromoSpider"
    allowed_domains = ["tunisiapromo.com"]
    start_urls = [
        'https://www.tunisiapromo.com/recherche?listing_type=4&property_type=1&region1=ANY&submit_listing=trouver+%21&property_search=a',
    ]
    custom_settings = {
        
        'DOWNLOAD_DELAY': 2, # 10 seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ######Condition d'arret
        file_path=os.getcwd()+"/AdsScrapper/first_run.csv"
        file_path = file_path.replace('/', '\\')
        with open(file_path, 'r', newline='') as file:
         first=True
         reader = csv.reader(file)
         for row in reader:
            website, date = row
            if website=="TP":
               first=False                           
        if first:
            website = 'TP'
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            with open(file_path, 'a', newline='') as file:
             writer = csv.writer(file)
             writer.writerow([website, date])
        self.first_run = first
     ####END
    

    def parse(self, response):
        links=response.css('a.headline::attr(href)').getall()
        # ########################
        Url_List=[]
        count=0
        if not self.first_run:
         b=BienImmobilier()
         

         for link in links:
            path=response.urljoin(link)
            
            if b.ReadbyUrl(path):
               count+=1
               continue
               
            else:
               Url_List.append(link)
               
        else: 
           Url_List=links

        
        
        for job in Url_List:
           yield response.follow(job, self.parse_listing)

        if len(Url_List)==0 or count>=4:
           raise scrapy.exceptions.CloseSpider("no more links to scrap")
        #############################

        next_page = response.css("p a:contains('Suivant')::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_listing(self, response):
        price = response.css('span.property_price::text').get().strip()
        reference = response.xpath('//span[text()="Référence :"]/following-sibling::span/text()').get().strip()
        property_type = response.xpath('//span[text()="Type du bien :"]/following-sibling::span/text()').get().strip()
        pieces = response.xpath('//span[text()="Nombre de pièce(s) :"]/following-sibling::span/text()').get().strip()
        salles_bain = response.xpath('//span[text()="Nombre de salle(s) de bain :"]/following-sibling::span/text()').get().strip()
        salles_eau = response.xpath('//span[text()="Nombre de salle(s) d\'eau :"]/following-sibling::span/text()').get().strip()
        annee_construction = response.xpath('//span[text()="Année de Construction :"]/following-sibling::span/text()').get().strip()
        surface_habitable = response.xpath('//span[text()="Surface habitable :"]/following-sibling::span/text()').get().strip()
        surface_totale = response.xpath('//span[text()="Surface Totale :"]/following-sibling::span/text()').get().strip()
        place_voiture = response.xpath('//span[text()="Nombre de place de Voiture :"]/following-sibling::span/text()').get().strip()
        num_etages = response.xpath('//span[text()="Numéro / Nombre d\'étages :"]/following-sibling::span/text()').get().strip()
        description = response.css(".clear p::text").get()
        clear_div = response.xpath('//div[@class="clear"]')
        text = clear_div.xpath('.//p').extract_first()
        text = ''.join(text)
        text = re.sub(r'<br\s*?>', '\n', text)     
        url=response.url    
        now = datetime.datetime.now()
        ScrapedDate = now.strftime("%d-%m-%y %H:%M:%S") 
        left_column = response.xpath('//div[@class="leftColumn"]')
        ajoute_date = left_column.xpath('.//span[text()="Ajoutée le :"]/following-sibling::text()').get()
        mise_a_jour_date = left_column.xpath('.//span[text()="Mise à jour le :"]/following-sibling::text()').get()
        clear_div = response.xpath('//div[@class="clear"]')
        location = clear_div.xpath('.//h2/text()').get()
        ville = location.replace("Maison à vendre à ", "")
        state=response.xpath('//strong[contains(text(), "Maison à vendre à")]/text()').get().split("à ")[-1]
        address_span = clear_div.xpath('.//span[text()="Adresse :"]')
        address = address_span.xpath('normalize-space(following-sibling::text())').get()  
        image_urls = response.xpath('//div[@id="gallery_container"]/span[@class="gal_img"]/a/@href').getall()
        img_src_list = []
        for photo in image_urls:         
            img_src_list.append("www.tunisiapromo.com/"+photo) 
        yield {
            'url':url,'price': price,'reference': reference,'property_type': property_type,'pieces': pieces, 'salles_bain': salles_bain,'salles_eau': salles_eau,'annee_construction': annee_construction,'surface_habitable': surface_habitable,'surface_totale': surface_totale,'place_voiture': place_voiture,'num_etages': num_etages,'description': text,'ScrapedDate':ScrapedDate,'ajoute_date':ajoute_date,'mise_a_jour_date':mise_a_jour_date,
            'location':location,'ville':ville,'state':state,'address':address,'images':img_src_list
        }

        row = {  'url':url,
            'price': price,
            'Code': reference,
            'property_type': property_type,
            'pieces': pieces,
            'salles_bain': salles_bain,
            'salles_eau': salles_eau,
            'annee_construction': annee_construction,
            'surface_habitable': surface_habitable,
            'surface_totale': surface_totale,
            'place_voiture': place_voiture,
            'num_etages': num_etages,
            'description': text+" "+property_type,
            'ScrapedDate':ScrapedDate,
            'date_insertion':ajoute_date,
            'date_Modification':mise_a_jour_date,
            'location':location,
            'ville':ville,
            'state':state,
            'address':address,
            'image_urls':img_src_list          
        }

        b=BienImmobilier()
        b.extractTunisiePromo(row)
        b.noneCheck()
        b.print_maison()
        b.SaveDb(b)
         

        # # define file path
        # file_path = "C:/Users/Lina/Desktop/TunisiePromo.csv"
        # # check if file exists, create it if it doesn't
        # if not os.path.exists(file_path):
        #     df.to_csv(file_path, index=False)
        # else:
        #     # read existing file into DataFrame
        #     existing_df = pd.read_csv(file_path)
            
        #     # append new DataFrame to existing file
        #     new_df = existing_df.append(df, ignore_index=True)
        #     new_df.to_csv(file_path, index=False)
