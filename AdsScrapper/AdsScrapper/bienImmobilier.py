import re
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime, timedelta




class BienImmobilier:
    client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
    db = client["AdsScrappers"]
    collection = db["Ads"]
    collectionH = db["AdsHistorisation"]
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
        print("total:",self.TotalDescp)
    
    def total_description(self):
       self.TotalDescp=" "
       if self.description:
        self.TotalDescp=self.TotalDescp+self.description+" "
        print(self.description)
        print(self.TotalDescp)
        print("\n\n\n\n\n\n\n\n*********************************************")

       if self.adresse:
        self.TotalDescp=self.TotalDescp+self.adresse+" "

       if self.country:
        self.TotalDescp=self.TotalDescp+self.country+" "
       if self.state:
        self.TotalDescp=self.TotalDescp+self.state+" "
       if self.zone:
        self.TotalDescp=self.TotalDescp+self.zone+" "
       if self.ville:
        self.TotalDescp=self.TotalDescp+self.ville
       for character in self.characteristicslist:
        self.TotalDescp=self.TotalDescp+" "+character+" "
 
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
        #self.TotalDescp=" "
        #self.total_description()

    def SaveDb(self,BI):
     # Set up a MongoDB client to connect to your Atlas cluster
      # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
      # # Access a database and a collection
      # db = client["AdsScrappers"]
      # collection = db["Ads"]
      property_dict = BI.__dict__
      filtered_dict = {k: v for k, v in property_dict.items() if v is not None}
      result = self.collection.insert_one(filtered_dict)
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
        # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        # db = client["AdsScrappers"]
        # collection = db["AdsHistorisation"]
        property_dict = BI.__dict__
        filtered_dict = {k: v for k, v in property_dict.items() if v is not None}
        result = self.collectionH.insert_one(filtered_dict)
      
  
    def ReadbyUrl(self,url):
        # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        # db = client["AdsScrappers"]
        # collection = db["Ads"]
        result = self.collection.find_one({'url': url})
        if result:
            if 'website' in result:
             self.website = result['website']

            if 'url' in result:
             self.url = result['url']

            if 'code' in result:
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

            if  'total_description'in result:
             self.TotalDescp=result['total_description']
            return True          
        else:
            return False 


    def readAll(self):
        # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        # db = client["AdsScrappers"]
        # collection = db["Ads"]
        cursor = self.collection.find({})
        datas = list(cursor)
        ListAll=[]


        for result in datas:
            BI=BienImmobilier()
           
            if 'website' in result:
             BI.website = result['website']
            if 'url'in result:
             BI.url = result['url']
            if 'code'in result:
             BI.code = result['code']
            if 'description'in result:
             BI.description = result['description']
            if 'price'in result:
             BI.price = result['price']
            if 'surfaceTotale'in result:
             BI.surfaceTotale = result['surfaceTotale']
            if 'surface_habitable'in result:
             BI.surface_habitable = result['surface_habitable']
            if 'adresse'in result:
             BI.adresse = result['adresse']
            if 'country'in result:
             BI.country = result['country']
            if 'state'in result:
             BI.state = result['state']
            if 'zone'in result:
             BI.zone = result['zone']
            if 'ville'in result:
             BI.ville = result['ville']
            if 'etage'in result:
             BI.etage = result['etage']
            if 'place_voiture'in result:
             BI.place_voiture = result['place_voiture']
            if 'characteristicslist'in result:
             BI.characteristicslist = result['characteristicslist']
            if 'nombre_de_chambre'in result:
             BI.nombre_de_chambre = result['nombre_de_chambre']
            if 'nombre_de_piece'in result:
             BI.nombre_de_piece = result['nombre_de_piece']
            if 'nombre_de_salle_de_bain'in result:
             BI.nombre_de_salle_de_bain = result['nombre_de_salle_de_bain']
            if 'datescraped'in result:
             BI.datescraped = result['datescraped']
            if 'dateinstered'in result:
             BI.dateinstered = result['dateinstered']
            if 'datemodified'in result:
             BI.datemodified = result['datemodified']
            if 'imagesurlslist'in result:
             BI.imagesurlslist = result['imagesurlslist']
            if 'anneeconstruction'in result:
             BI.anneeconstruction = result['anneeconstruction']
            if 'total_description'in result:
             BI.TotalDescp=result['total_description']
            ListAll.append(BI.__dict__)

        return ListAll 
    
    
    def readAll_TA_TV(self):
        # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
        # db = client["AdsScrappers"]
        # collection = db["Ads"]
        query = {"$or": [{"website": "tunisie-vente.com"}, {"website": "tunisie-annonce.com"}]}
        
        cursor = self.collection.find(query)
        datas = list(cursor)
        ListAll=[]


        for result in datas:
            BI=BienImmobilier()
           
            if 'website' in result:
             BI.website = result['website']
            if 'url'in result:
             BI.url = result['url']
            if 'code'in result:
             BI.code = result['code']
            if 'description'in result:
             BI.description = result['description']
            if 'price'in result:
             BI.price = result['price']
            if 'surfaceTotale'in result:
             BI.surfaceTotale = result['surfaceTotale']
            if 'surface_habitable'in result:
             BI.surface_habitable = result['surface_habitable']
            if 'adresse'in result:
             BI.adresse = result['adresse']
            if 'country'in result:
             BI.country = result['country']
            if 'state'in result:
             BI.state = result['state']
            if 'zone'in result:
             BI.zone = result['zone']
            if 'ville'in result:
             BI.ville = result['ville']
            if 'etage'in result:
             BI.etage = result['etage']
            if 'place_voiture'in result:
             BI.place_voiture = result['place_voiture']
            if 'characteristicslist'in result:
             BI.characteristicslist = result['characteristicslist']
            if 'nombre_de_chambre'in result:
             BI.nombre_de_chambre = result['nombre_de_chambre']
            if 'nombre_de_piece'in result:
             BI.nombre_de_piece = result['nombre_de_piece']
            if 'nombre_de_salle_de_bain'in result:
             BI.nombre_de_salle_de_bain = result['nombre_de_salle_de_bain']
            if 'datescraped'in result:
             BI.datescraped = result['datescraped']
            if 'dateinstered'in result:
             BI.dateinstered = result['dateinstered']
            if 'datemodified'in result:
             BI.datemodified = result['datemodified']
            if 'imagesurlslist'in result:
             BI.imagesurlslist = result['imagesurlslist']
            if 'anneeconstruction'in result:
             BI.anneeconstruction = result['anneeconstruction']
            if 'total_description'in result:
             BI.TotalDescp=result['total_description']
            ListAll.append(BI.__dict__)

        return ListAll 

    def deleteduplicate_Ta_TV(self):
      # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
      # db = client["AdsScrappers"]
      # collection = db["Ads"]
      delete_result = self.collection.delete_many({"code": self.code, "website": self.website})
      return delete_result.deleted_count
    
    def deleteduplicate_Historisation(self):
      # client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
      # db = client["AdsScrappers"]
      # collection = db["AdsHistorisation"]
      delete_result = self.collectionH.delete_one({"code": self.code})
      return delete_result.deleted_count
    
    def Readtest(self,code):      
        result = self.collection.find_one({'code': code})
        return result['code']
    
    def Delete_6months(self):
      three_months_ago = datetime.utcnow() - timedelta(days=90)
      delete_result = self.collection.delete_many({"dateinstered": {"$lt": three_months_ago}})
      return delete_result.deleted_count
    
    def FindOneTA_TV(self,code,web):     
      query = {"code": code, "website": web}
      result = self.collection.find_one(query)

      if result:
          return True
      else:
          return False
      