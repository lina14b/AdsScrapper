import scrapy
import pandas as pd
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.settings import Settings

class TunisieventespiderSpider(scrapy.Spider):
    name = "TunisieVenteSpider"
    allowed_domains = ["tunisie-vente.com"]
    start_urls = ["http://www.tunisie-vente.com/ListeOffres.asp"]
    base_url = "http://www.tunisie-vente.com/"
    
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10,  # set the maximum number of items to extract
        'DOWNLOAD_DELAY': 10 # 10 seconds delay

    }

    def parse(self, response):
        # Extract the URLs of all the listings on the page
        listings = response.css(".liste").css(".liste_offre a::attr(href)").getall()
        
        for listing in listings:
            # Follow the link to the listing page and extract the information
            yield Request(url=self.base_url+listing, callback=self.parse_listing)

    def parse_listing(self, response):
        # Extract the information from the listing page
        sel = Selector(response)
        localisation = sel.css("#localisation::text").get()
        adresse = sel.css("#adresse::text").get()
        surface = sel.css("#surface::text").get()
        prix = sel.css("#prix::text").get()
        texte = sel.css("#texte::text").get()
        date_insertion = sel.css("#date_ins::text").get()
        date_modification = sel.css("#date_maj::text").get()
        photos = sel.css("#photos::attr(src)").getall()
        
        # Return the extracted information as a dictionary
        yield {
            "url": response.url,
            "localisation": localisation,
            "adresse": adresse,
            "surface": surface,
            "prix": prix,
            "texte": texte,
            "date_insertion": date_insertion,
            "date_modification": date_modification,
            "photos": photos
        }
        
        # Save the extracted information to an Excel file
        df = pd.DataFrame([{
            "url": response.url,
            "localisation": localisation,
            "adresse": adresse,
            "surface": surface,
            "prix": prix,
            "texte": texte,
            "date_insertion": date_insertion,
            "date_modification": date_modification,
            "photos": photos
        }])
        
        with pd.ExcelWriter("tunisievente.xlsx", mode="a") as writer:
            df.to_excel(writer, index=False)
