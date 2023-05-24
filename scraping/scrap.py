import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

data=[]

class ListingType():
    def __init__(self): 
        self.titre = None 
        self.category = None
        # self.description = None
        self.place = None
        self.prix = None

page_count = 0
while page_count < 2:

    url = "https://www.tayara.tn/search/?category=Immobilier?page=%d" %(page_count)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    property_listings = soup.find_all("div", class_="p-0 px-3 z-10 flex-none -mt-1")
    
    for property_listing in property_listings:
        listing=ListingType()
        category = property_listing.find("span",class_="truncate text-3xs md:text-xs lg:text-xs w-3/5 font-medium text-neutral-500").text
        if (category in ["Colocations", "Maisons et Villas", "Magasins, Commerces et Locaux industriels", "Locations de vacances", "Appartements", "Bureaux et Plateaux", "Autres Immobiliers", "Terrains et Fermes", "Meubles et Décoration"]):
            listing.category = category
            # description = property_listing.find("h2",class_="card-title font-arabic text-sm font-medium leading-5 text-gray-800 max-w-min min-w-full line-clamp-2 mb-2 mt-1").text
            # listing.description = description
            place= property_listing.find("span",class_="line-clamp-1 truncate text-3xs md:text-xs lg:text-xs w-3/5 font-medium text-neutral-500").text
            listing.place = place
            prix= property_listing.select_one("data",class_="text-red-600 font-bold font-arabic  undefined").attrs.get("value", None)
            listing.prix = prix
            titre= property_listing.find("h2",class_="card-title font-arabic text-sm font-medium leading-5 text-gray-800 max-w-min min-w-full line-clamp-2 mb-2 mt-1").text
            listing.titre = titre
            
            data.append(listing)

    page_count += 1

# print(len(data))

file = open('scraped.csv', 'w', encoding="utf-8")
writer = csv.writer(file)
writer.writerow(['titre', 'Categorie', 'Ville', 'prix'])

for listing in data:
    writer.writerow([listing.titre, listing.category, listing.place, listing.prix])

df=pd.read_csv('scraped.csv')

df