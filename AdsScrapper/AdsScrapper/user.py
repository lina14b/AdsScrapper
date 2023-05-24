from pymongo import MongoClient
import pymongo
from bienImmobilier import BienImmobilier
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

class User:
    client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
    db = client["AdsScrappers"]
    collectionUser = db["User"]
    def __init__(self,id=None,email=None,prixmin=None,prixmax=None,surfmin=None,surfmax=None,state=None,ville=None,typeb=None,saved=[],savedids=[]):
        self.id = id
        self.email = email
        self.priceMin=prixmin
        self.priceMax=prixmax
        self.surfaceMin=surfmin
        self.surfaceMax=surfmax
        if state:
         self.state=state.lower()
        if ville:
         self.ville=ville.lower()
        if typeb:
         self.typeb=typeb.lower()
        self.saved = saved
        self.savedIds = savedids
    
    def save(self):
      print(self.id)
      property_dict = self.__dict__
      filtered_dict = {k: v for k, v in property_dict.items() if v is not None}
      result = self.collectionUser.insert_one(filtered_dict)

    def update(self):
        print(self.id)
        property_dict = self.__dict__
        filtered_dict = {k: v for k, v in property_dict.items() if v is not None}
        self.collectionUser.update_one({"id": self.id}, {"$set": filtered_dict}, upsert=True)
        self.readone(self.id)

    def readone(self,id):
        result = self.collectionUser.find_one({'id': id})
        test=False
        if result:
            if 'id' in result:
             self.id = result['id']
             test=True

            if 'email' in result:
             self.email = result['email']

            if 'priceMin' in result:
             self.priceMin = result['priceMin']

            if 'priceMax'in result:
             self.priceMax = result['priceMax']

            if 'surfaceMin'in result:
             self.surfaceMin = result['surfaceMin']

            if 'surfaceMax'in result:
             self.surfaceMax = result['surfaceMax']

            if 'state'in result:
             self.state = result['state']

            if 'ville'in result:
             self.ville = result['ville']
            
            if 'typeb'in result:
             self.typeb = result['typeb']

            if 'saved'in result:
             self.savedIds = result['savedIds']
             self.saved=result['saved']
        return test

  
    def AddSaved(self,user,id):
      self.savedIds.append(id)
      b=BienImmobilier()
      b.ReadbyId(id)
      x=b.__dict__
      self.saved.append(x)
     
      user.update()

    def RemoveSaved(self,user,id):
      self.savedIds.remove(id)
      object_id = ObjectId(id)

      filtered_list = []
      for item in self.saved:
        if item['code']!=object_id:
          filtered_list.append(item)
      self.saved=filtered_list

      self.update()   
    
    def readAll(self,):
       cursor = self.collectionUser.find({})
       datas = list(cursor)
       ListAll=[]
       for result in datas:
        U=User()
        if result:
            if 'id' in result:
             U.id = result['id']

            if 'email' in result:
             U.email = result['email']

            if 'priceMin' in result:
             U.priceMin = result['priceMin']

            if 'priceMax'in result:
             U.priceMax = result['priceMax']

            if 'surfaceMin'in result:
             U.surfaceMin = result['surfaceMin']

            if 'surfaceMax'in result:
             U.surfaceMax = result['surfaceMax']

            if 'state'in result:
             U.state = result['state']

            if 'ville'in result:
             U.ville = result['ville']
            ListAll.append(U)
       return ListAll
       
    def Notify(self,im,id):
      Users=self.readAll()
      
      teststate=False
      testpriceMin=False
      testpriceMax=False
      testsurfMin=False
      testsurfMax=False
      testville=False
      testzone=False
      testdescription=False
      
      print(len(Users))
      for one in Users:

        u=User()
        u=one
        print(u)
        print(u.email)
        if u.state and im.state and u.state==im.state: teststate=True
        if u.priceMin and im.price and u.priceMin<=im.price:testpriceMin=True
        if u.priceMax and im.price and u.priceMax>=im.price:testpriceMax=True
        if u.surfaceMin and im.surfaceTotale and u.surfaceMin<=im.surfaceTotale:testsurfeMin=True
        if u.surfaceMax and im.surfaceTotale and u.surfaceMax>=im.surfaceTotale:testsurfeMax=True
        if u.ville and im.ville and u.ville==im.ville:testville=True        
        if u.ville and im.zone and u.zone==im.zone:zone=True       
        if u.ville and im.description and u.ville in im.description: testdescription=True
        if teststate and testpriceMax and (testville or testzone or testdescription):
         u.SendEmail(id)
        
       


      

    def SendEmail(self,id):

      sender_email = 'edsoftad@gmail.com'
      sender_password = 'jgsvvxkwvkcfzssu'
      recipient_email = self.email
      subject =  "New house for you!!"
      message = 'Check out this offer it suits your needs '+"http://127.0.0.1:8000/details?item="+id
      msg = MIMEMultipart()
      msg['From'] = sender_email
      msg['To'] = recipient_email
      msg['Subject'] = subject

      msg.attach(MIMEText(message, 'plain'))

      try:
          # Establish a secure connection with the SMTP server
          with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
              # Login to the sender's email account
              server.login(sender_email, sender_password)
              # Send the email
              time.sleep(2)
              server.send_message(msg)
          print('Email sent successfully.')
      except Exception as e:
          print('An error occurred while sending the email:', str(e),e)
      