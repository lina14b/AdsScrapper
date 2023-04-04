import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin



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
        
        'DOWNLOAD_DELAY':  10, # seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def parse(self, response):

        links = response.css('div.gallery-title a::attr(href)').getall()
        
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
       
        next_page = response.css('li a.ajax-page-link[aria-label=""]::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

        
    def parse_details(self, response):
        
        sel = Selector(response)

        key_title = response.css('div.key-title')
        title_text = key_title.css('h1::text').get().split('-')
        categorie = title_text[0].strip()
        
        price_div = response.css('div.key-price-div')
        price = price_div.css('a[itemprop="price"]::text').get().strip()

        address = response.css('div.key-address::text').get().strip()
        
        data_item_row = response.css('div.data-item-row')

        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Nombre de pièces':
                pieces = row.css('.data-item-value span::text').get() 
        
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Nombre de chambres':
                chambres = row.css('.data-item-value span::text').get()

        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Nombre salles de bain':
                Salles_de_bain = row.css('.data-item-value span::text').get()

        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'm²':
                Surface = row.css('.data-item-value span::text').get()
                Surface = Surface +label

        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Surface constructible (m²)':
                surface_constructible = row.css('.data-item-value span::text').get()
        
        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Places de parking':
                Parking = row.css('.data-item-value span::text').get()

        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Nombre d''étages':
                Etage = row.css('.data-item-value span::text').get()
            elif label == 'Etage':
                Etage = row.css('.data-item-value span::text').get()
               

        for row in data_item_row:
            label = row.css('.data-item-label span::text').get()
            if label == 'Nombre de WC':
                Salles_deau  = row.css('.data-item-value span::text').get()

        description = response.css("#ListingFullLeft_ctl01_DescriptionDivShort.desc-short ::text").getall()
        description = "".join(description).replace('\n','').replace('\r','')
   
        Equipement = []
        for feature_item in response.css("div.features-container span.feature-item"):
            feature = feature_item.css("::text").get()
            Equipement.append(feature)

        image_urls = response.css('#Images img::attr(src)').getall()
        




