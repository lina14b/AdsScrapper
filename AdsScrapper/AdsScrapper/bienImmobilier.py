import re
from datetime import datetime
from pymongo import MongoClient



class BienImmobilier:
    def __init__(self):
        self.website = None
        self.url = None
        self.code = None
        self.description = None
        self.price = None
        self.surfaceTotale = None
        self.surface_habitable = None
        self.adresse = None
        self.country = None
        self.state = None
        self.zone = None
        self.ville = None
        self.etage = None
        self.place_voiture = None
        self.characteristicslist = []
        self.nombre_de_chambre = None
        self.nombre_de_piece = None
        self.nombre_de_salle_de_bain = None
        self.datescraped = None
        self.dateinstered = None
        self.datemodified = None
        self.imagesurlslist = []
        self.anneeconstruction = None
        self.TotalDescp=None
   
    def extractTunisieVente(self,row):
    #Url
     self.website="tunisie-vente.com"
     self.url=row['url']

    #Code 
     row['Code']=row['Code'].replace(" ", "")
     if row['Code']:
      self.code=int(row['Code'], 10)
    #Desc
     if row['description'] and not row['description'].isspace():
      self.description=row['description']   
    ##price
     if  row['price']:
      numeric_only = re.sub(r'[^\d]', '', row['price'])
      numeric_only=int(numeric_only, 10)
      if numeric_only<1000:
       numeric_only=numeric_only*1000  
      self.price = numeric_only
     
    #surface
     if row['surface']:
      numeric_only = re.sub(r'[^\d]', '', row['surface']) 
      self.surfaceTotale = numeric_only
     
     self.adresse =  row['adresse']
     location=row['localisation']
     self.country = 'Tunisie'
     self.state = None
     self.zone = location[2]
     self.ville = location[4]
     self.etage = None
     self.place_voiture = None
     self.characteristicslist = []
     self.nombre_de_chambre = None
     self.nombre_de_piece = None
     self.nombre_de_salle_de_bain = None
     self.datescraped = row['ScrapedDate']
     row['date_insertion']=row['date_insertion'].replace(" ", "")
     row['date_insertion']=row['date_insertion'].replace(":", "")
     row['date_insertion']=row['date_insertion'].replace("\xa0", "")
     if row['date_insertion']:
      self.dateinstered = datetime.strptime(row['date_insertion'], '%d/%m/%Y') 

     if not row['date_Modification'] or row['date_Modification'].isspace():
       row['date_Modification']=row['date_insertion']

     row['date_Modification']=row['date_Modification'].replace(" ", "")
     row['date_Modification']=row['date_Modification'].replace(":", "")
     row['date_Modification']=row['date_Modification'].replace("\xa0", "")
     if row['date_Modification']:
      self.datemodified = datetime.strptime(row['date_Modification'], '%d/%m/%Y') 

     self.imagesurlslist = row['image_urls']
     self.total_description()
     
    def extractTunisiePromo(self,row):
     #Url
     self.website="tunisiapromo.com"
     self.url=row['url']

     num = row['url'].split('-')[-1].split('.')[0]
     num=num.replace("z", "")

     self.code=int(num, 10)
     row['description']=row['description'].replace("<p>", "")
     row['description']=row['description'].replace("</p>", "")  
     self.description=row['description']  
     
     ##price
     numeric_only = re.sub(r'[^\d]', '', row['price'])
     numeric_only=int(numeric_only, 10)
     if numeric_only<1000:
       numeric_only=numeric_only*1000   
     self.price = numeric_only
    
     #surface
     if row['surface_totale']:
        numeric_only = re.sub(r'[^\d]', '', row['surface_totale'])
             
        self.surfaceTotale = numeric_only
     if row['surface_habitable']:
      numeric_only = re.sub(r'[^\d]', '', row['surface_habitable'])
       
      self.surface_habitable = numeric_only
   
     self.adresse =  row['address']
     self.country = 'Tunisie'
     self.state = row['state']
     self.zone = None
     self.ville = row['ville']
     if row['num_etages']:
      numeric_only = re.sub(r'[^\d]', '', row['num_etages'])
      
      self.etage = numeric_only
     if row['place_voiture']:
      numeric_only = re.sub(r'[^\d]', '', row['place_voiture'])
      
      self.place_voiture = numeric_only

     self.characteristicslist = []
     self.nombre_de_chambre = None
     if row['pieces']:
      numeric_only = re.sub(r'[^\d]', '', row['pieces'])
      
      self.nombre_de_piece = numeric_only
     if row['salles_bain']:
      numeric_only = re.sub(r'[^\d]', '', row['salles_bain'])
      
      self.nombre_de_salle_de_bain = numeric_only
     
     self.datescraped = row['ScrapedDate']
     if row['date_insertion']:
      row['date_insertion']=row['date_insertion'].replace(" ", "")
      row['date_insertion']=row['date_insertion'].replace(":", "")
      row['date_insertion']=row['date_insertion'].replace("\xa0", "")
      row['date_insertion']=row['date_insertion'].replace("\n", "")
      self.dateinstered = datetime.strptime(row['date_insertion'], '%d/%m/%Y') 

     if not row['date_Modification'] or row['date_Modification'].isspace():
       row['date_Modification']=row['date_insertion']
     if row['date_Modification']:
      row['date_Modification']=row['date_Modification'].replace(" ", "")
      row['date_Modification']=row['date_Modification'].replace(":", "")
      row['date_Modification']=row['date_Modification'].replace("\xa0", "")
      row['date_Modification']=row['date_Modification'].replace("\n", "")
     self.datemodified = datetime.strptime(row['date_Modification'], '%d/%m/%Y') 

     self.imagesurlslist = row['image_urls']

     numeric_only = re.sub(r'[^\d]', '', row['annee_construction'])
     self.anneeconstruction=numeric_only

     self.total_description()
    
    def extractTPS(self,row):
     self.website="tps-immobiliere.com"
     self.url=row['url']

     self.code=int(row['Code'], 10)

     self.description=row['description']  
     
     ##price
     numeric_only = re.sub(r'[^\d]', '', row['price'])
     numeric_only=int(numeric_only, 10)
     if numeric_only<1000:
       numeric_only=numeric_only*1000   
     self.price = numeric_only
     
     #surface
     if row['surface_totale']:
        numeric_only = re.sub(r'[^\d]', '', row['surface_totale'])     
        self.surfaceTotale = numeric_only
     if row['surface_habitable']:
        numeric_only = re.sub(r'[^\d]', '', row['surface_habitable']) 
        self.surface_habitable = numeric_only
   
     self.adresse =  None
     self.country = None
     self.state = None
     self.zone = row['localisation']
     self.ville = None

     self.etage = None
     self.place_voiture = None

     self.characteristicslist = []
     for item in row['characteristics']:
      clean_item = item.strip()
      if clean_item:
        self.characteristicslist.append(clean_item)

     self.nombre_de_chambre = row['Nb_chambre']
     self.nombre_de_piece = row['Nb_piece']
     self.nombre_de_salle_de_bain = row['Nb_SalleBain']
     
     self.datescraped = row['ScrapedDate']
     
     self.dateinstered =self.datescraped 
     self.datemodified = self.datescraped  

     self.imagesurlslist = row['image_urls']

     self.total_description()
   
    def extractTA(self,row):
     self.website="tunisie-annonce.com"
     self.url=row['url']
     self.code=int(row['Code'], 10)
     self.description=row['description']   
     ##price
     numeric_only = re.sub(r'[^\d]', '', row['price'])
     numeric_only=int(numeric_only, 10)
     if numeric_only<1000:
       numeric_only=numeric_only*1000   
     self.price = numeric_only
     #surface
     numeric_only = re.sub(r'[^\d]', '', row['surface']) 
     self.surfaceTotale = numeric_only
     self.surface_habitable = None
     self.adresse =  row['adresse']
     self.country = 'Tunisie'
     self.state = row['state']
     self.zone = row['region']
     self.ville = row['ville']
     self.etage = None
     self.place_voiture = None
     self.characteristicslist = []
     self.nombre_de_chambre = None
     self.nombre_de_piece = None
     self.nombre_de_salle_de_bain = None
     self.datescraped = row['ScrapedDate']
     row['date_insertion']=row['date_insertion'].replace(" ", "")
     row['date_insertion']=row['date_insertion'].replace(":", "")
     row['date_insertion']=row['date_insertion'].replace("\xa0", "")
     self.dateinstered = datetime.strptime(row['date_insertion'], '%d/%m/%Y') 

     if not row['date_Modification'] or row['date_Modification'].isspace():
       row['date_Modification']=row['date_insertion']
     row['date_Modification']=row['date_Modification'].replace(" ", "")
     row['date_Modification']=row['date_Modification'].replace(":", "")
     row['date_Modification']=row['date_Modification'].replace("\xa0", "")
     self.datemodified = datetime.strptime(row['date_Modification'], '%d/%m/%Y') 

     self.imagesurlslist = row['image_urls']
     self.total_description()
    
    def extractBnb(self,row):
     self.website="bnb.tn"
     self.url=row['url']

     self.code=int(row['Code'], 10)

     self.description=row['description']  
     
     ##price
     row['price']=row['price'].replace(",", "")
     numeric_only = re.sub(r'[^\d]', '', row['price'])
     numeric_only=int(numeric_only, 10)
     if numeric_only<1000:
       numeric_only=numeric_only*1000   
     self.price = numeric_only
     
     #surface
     if row['surface_totale']:
        numeric_only = re.sub(r'[^\d]', '', row['surface_totale'])     
        self.surfaceTotale = numeric_only
     if row['surface_habitable']:
        numeric_only = re.sub(r'[^\d]', '', row['surface_habitable']) 
        self.surface_habitable = numeric_only
   
     self.adresse =  None
     self.country = None
     self.state = row['localisation']
     self.zone = row['localisation']
     self.ville = None


     self.nombre_de_chambre = row['Nb_chambre']
     self.nombre_de_piece = None
     self.nombre_de_salle_de_bain = row['Nb_SalleBain']
     
     self.datescraped = row['ScrapedDate']
     
     self.dateinstered =self.datescraped 
     self.datemodified = self.datescraped  

     self.imagesurlslist = row['image_urls']

     self.total_description()

    def print_maison(self):
        print("Website:", self.website)
        print("URL:", self.url)
        print("Code:", self.code)
        print("Description:", self.description)
        print("Price:", self.price)
        print("Total Surface:", self.surfaceTotale)
        print("Living Area Surface:", self.surface_habitable)
        print("Address:", self.adresse)
        print("Country:", self.country)
        print("State:", self.state)
        print("Zone:", self.zone)
        print("City:", self.ville)
        print("Floor:", self.etage)
        print("Parking Space:", self.place_voiture)
        print("Characteristics:", self.characteristicslist)
        
        print("Number of Bedrooms:", self.nombre_de_chambre)
        print("Number of Bedrooms:", self.nombre_de_chambre)

        print("Number of Rooms:", self.nombre_de_piece)
        
        print("Number of Rooms:", self.nombre_de_piece)
        print("Number of Bathrooms:", self.nombre_de_salle_de_bain)
        print("Date Scraped:", self.datescraped)
        print("Date Inserted:", self.dateinstered)
        print("Date Modified:", self.datemodified)
        print("Image URLs:", self.imagesurlslist)
        print("Construction Year:", self.anneeconstruction)
        print("total:",self.total_description)
    
    def total_description(self):
       self.total_description=""
       if self.description:
        self.total_description=self.total_description+self.description+" "

       if self.adresse:
        self.total_description=self.total_description+self.adresse+" "

       if self.country:
        self.total_description=self.total_description+self.country+" "
       if self.state:
        self.total_description=self.total_description+self.state+" "
       if self.zone:
        self.total_description=self.total_description+self.zone+" "
       if self.ville:
        self.total_description=self.total_description+self.ville
    
      
       for character in self.characteristicslist:
        self.total_description=self.total_description+" "+character+" "
 
    def noneCheck(self):
        if not self.website or self.website.isspace():
         self.website = None
        
        if not self.url or self.url.isspace():
         self.url = None

        if not self.code :
         self.code = None

        if not self.description or self.description.isspace():
         self.description = None

        if not self.price :
         self.price = None

        if not self.surfaceTotale or self.surfaceTotale.isspace():
         self.surfaceTotale = None
        else:
         self.surfaceTotale=int(self.surfaceTotale, 10)

        if not self.surface_habitable or self.surface_habitable.isspace() :
         self.surface_habitable = None
        else:
         self.surface_habitable=int(self.surface_habitable, 10)

        if not self.adresse or self.adresse.isspace():
         self.adresse = None

        if not self.country or self.country.isspace():
         self.country = None

        if not self.state or self.state.isspace():
         self.state = None

        if not self.zone or self.zone.isspace():
         self.zone = None

        if not self.ville or self.ville.isspace() :
         self.ville = None

        if not self.etage or self.etage.isspace():
         self.etage = None
        else:
         self.etage=int(self.etage, 10)

        if not self.place_voiture or self.place_voiture.isspace():
         self.place_voiture = None 
        else:
         self.place_voiture=int(self.place_voiture, 10)

        if not self.nombre_de_chambre or self.nombre_de_chambre.isspace():
         self.nombre_de_chambre = None
        else:
         self.nombre_de_chambre=int(self.nombre_de_chambre, 10)

        if not self.nombre_de_piece or self.nombre_de_piece.isspace():
         self.nombre_de_piece = None
        else:
         self.nombre_de_piece=int(self.nombre_de_piece, 10)

        if not self.nombre_de_salle_de_bain or self.nombre_de_salle_de_bain.isspace():
         self.nombre_de_salle_de_bain = None
        else:
         self.nombre_de_salle_de_bain=int(self.nombre_de_salle_de_bain, 10)

        if not self.datescraped :
         self.datescraped = None
        else:
         self.datescraped= datetime.now()

        if not self.dateinstered :
         self.dateinstered = None

        if not self.datemodified :
         self.datemodified = None

        if not self.anneeconstruction or self.anneeconstruction.isspace():
         self.anneeconstruction = None
        else:
         self.anneeconstruction=int(self.anneeconstruction, 10)

        if not self.total_description :
         self.TotalDescp=None

    def SaveDb(self,BI):
     # Set up a MongoDB client to connect to your Atlas cluster
      client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
      # Access a database and a collection
      db = client["AdsScrappers"]
      collection = db["Ads"]
      property_dict = BI.__dict__
      filtered_dict = {k: v for k, v in property_dict.items() if v is not None}
      result = collection.insert_one(filtered_dict)
      self.SaveDb_Historisation()
    
    def SaveDb_Historisation(self):
      if self.price and self.dateinstered and self.country and self.surfaceTotale and self.ville:
        BI=BienImmobilier()
        BI.code=self.code
        BI.price=self.price
        BI.dateinstered=self.dateinstered
        BI.country=self.country
        BI.ville=self.ville
        BI.surfaceTotale=self.surfaceTotale
        BI.characteristicslist=None
        BI.imagesurlslist=None
        client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        db = client["AdsScrappers"]
        collection = db["AdsHistorisation"]
        property_dict = BI.__dict__
        filtered_dict = {k: v for k, v in property_dict.items() if v is not None}
        result = collection.insert_one(filtered_dict)
      
  
    def ReadbyUrl(self,url):
        client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        db = client["AdsScrappers"]
        collection = db["Ads"]
        result = collection.find_one({'url': url})
        if result:
            if 'website' in result:
             self.website = result['website']

            if result['url'] in result:
             self.url = result['url']

            if result['code'] in result:
             self.code = result['code']

            if result['description']in result:
             self.description = result['description']

            if 'price'in result:
             self.price = result['price']

            if 'surfaceTotale' in result:
             self.surfaceTotale = result['surfaceTotale']

            if 'surface_habitable' in result:
             self.surface_habitable = result['surface_habitable']

            if 'adresse' in result:
             self.adresse = result['adresse']

            if 'country' in result:
             self.country = result['country']

            if 'state' in result:
             self.state = result['state']

            if 'zone' in result:
             self.zone = result['zone']

            if 'ville' in result:
             self.ville = result['ville']

            if 'etage' in result:
             self.etage = result['etage']

            if 'place_voiture' in result:
             self.place_voiture = result['place_voiture']

            if 'characteristicslist' in result:
             self.characteristicslist = result['characteristicslist']

            if 'nombre_de_chambre' in result:
             self.nombre_de_chambre = result['nombre_de_chambre']

            if 'nombre_de_piece' in result:
             self.nombre_de_piece = result['nombre_de_piece']

            if 'nombre_de_salle_de_bain' in result:
             self.nombre_de_salle_de_bain = result['nombre_de_salle_de_bain']

            if 'datescraped' in result:
             self.datescraped = result['datescraped'] 

            if  'dateinstered'in result:
             self.dateinstered = result['dateinstered']

            if  'datemodified'in result:
             self.datemodified = result['datemodified']

            if  'imagesurlslist'in result:
             self.imagesurlslist = result['imagesurlslist']

            if  'anneeconstruction'in result:
             self.anneeconstruction = result['anneeconstruction']

            if  'TotalDescp'in result:
             self.TotalDescp=result['TotalDescp']
            return True          
        else:
            return False 


    def readAll(self):
        client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        db = client["AdsScrappers"]
        collection = db["Ads"]
        cursor = collection.find({})
        datas = list(cursor)
        ListAll=[]


        for result in datas:
            BI=BienImmobilier()
           
            if result['website']:
             BI.website = result['website']
            if result['url']:
             BI.url = result['url']
            if result['code']:
             BI.code = result['code']
            if result['description']:
             BI.description = result['description']
            if result['price']:
             BI.price = result['price']
            if result['surfaceTotale']:
             BI.surfaceTotale = result['surfaceTotale']
            if result['surface_habitable']:
             BI.surface_habitable = result['surface_habitable']
            if result['adresse']:
             BI.adresse = result['adresse']
            if result['country']:
             BI.country = result['country']
            if result['state']:
             BI.state = result['state']
            if result['zone']:
             BI.zone = result['zone']
            if result['ville']:
             BI.ville = result['ville']
            if result['etage']:
             BI.etage = result['etage']
            if result['place_voiture']:
             BI.place_voiture = result['place_voiture']
            if result['characteristicslist']:
             BI.characteristicslist = result['characteristicslist']
            if result['nombre_de_chambre']:
             BI.nombre_de_chambre = result['nombre_de_chambre']
            if result['nombre_de_piece']:
             BI.nombre_de_piece = result['nombre_de_piece']
            if result['nombre_de_salle_de_bain']:
             BI.nombre_de_salle_de_bain = result['nombre_de_salle_de_bain']
            if result['datescraped']:
             BI.datescraped = result['datescraped']
            if result['dateinstered']:
             BI.dateinstered = result['dateinstered']
            if result['datemodified']:
             BI.datemodified = result['datemodified']
            if result['imagesurlslist']:
             BI.imagesurlslist = result['imagesurlslist']
            if result['anneeconstruction']:
             BI.anneeconstruction = result['anneeconstruction']
            if result['TotalDescp']:
             BI.TotalDescp=result['TotalDescp']
            ListAll.append(BI, ignore_index=True)
        
