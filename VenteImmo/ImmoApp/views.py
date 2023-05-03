from django.shortcuts import render
from .models import Immo
from pymongo import MongoClient


def ImmoApp(request):

  client = MongoClient('mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test?retryWrites=true&w=majority')

  db = client['AdsScrappers']

  my_collection = db['Ads']
 
  data = my_collection.find({})
  listt=list(data)
  #data = Immo.objects.all()
  print("\n\n***********************")
  print(len(listt))
  context = {'data': listt}
  return render(request, 'Home.html', context)




  

