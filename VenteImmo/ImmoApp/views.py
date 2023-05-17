# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from pymongo import MongoClient, ASCENDING
from django.conf import settings
from pymemcache.client.base import Client
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
import sys
import datetime
import time 
sys.path.append('C:/Users/Lina/Desktop/AdsScrapper/AdsScrapper/AdsScrapper/AdsScrapper')
from bienImmobilier import BienImmobilier

def ImmoApp(request):
  template = loader.get_template('Home.html')
  return HttpResponse(template.render())



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

my_data = []
ville=[]
def populate_data():
    b=BienImmobilier()
    global my_data
    MONGO_URI = 'mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(MONGO_URI)
    db = client['AdsScrappers']
    collection = db['Ads']
    
    distinct_values = list(collection.distinct("state", {"ville": {"$exists": True}}))
    print(distinct_values)
    global ville
    ville=distinct_values
    my_data = b.readAll()
    print("done")
    time.sleep(10)
    date_format1 = '%d-%m-%Y %H:%M:%S'
    date_format2 = '%d-%m-%y %H:%M:%S'
    for item in my_data:
      if isinstance(item['dateinstered'], str):
        try:
         item['dateinstered'] = datetime.datetime.strptime(item['dateinstered'], date_format1)
        except ValueError:
         try:
             item['dateinstered'] = datetime.datetime.strptime(item['dateinstered'], date_format2)
         except ValueError:
             continue


def index(request):
    if not my_data:
        print("populate data")
        populate_data()
    page_number = request.GET.get('page', 1)
    page_number = int(page_number)
    cached_data = cache.get(f'my_data_{page_number}')
    data=[]
    if cached_data is not None:
        # Use the cached data
        data = cached_data
    else:
        MONGO_URI = 'mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(MONGO_URI)
        db = client['AdsScrappers']
        collection = db['Ads']

        page_size = 21

        all_data = my_data

        paginator = Paginator(all_data, page_size)

        try:
            data = paginator.page(page_number)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        # Cache the data
        cache.set(f'my_data_{page_number}', data,timeout=3600)
       
    return render(request, 'Home.html', {'data': data, 'page': page_number,'state':ville})
def sort(request):
    global my_data
    print(len(my_data))
    print(my_data[10])
    item=my_data[10]
    print(item['datescraped'])
    print(type(item['dateinstered']))
    print("...")
    i=0
    for item in my_data[:1000]:
     
     if isinstance(item['dateinstered'], str):
        print(i,item['dateinstered'])
     i+=1
    data=[]
    if  my_data:
        if 'up-arrow' in request.GET:
            for item in my_data:
              if item['price'] is not None:
                  if item['price']>1000 :
                   data.append(item)
            sorted_data = sorted(data, key=lambda x: x['price'])
            my_data=sorted_data

            print("up")
        elif 'down-arrow' in request.GET:
            for item in my_data:
              if item['price'] is not None:
                  if item['price']>1000 :
                   data.append(item)
                 
            sorted_data = sorted(data, key=lambda x: x['price'], reverse=True)
            my_data=sorted_data
        if 'old' in request.GET:
            # for item in my_data:
            #   if item['dateinstered'] is not None:
            #     #   if item['price']>1000 :
                #    data.append(item)
            sorted_data = sorted(my_data, key=lambda x: x['datescraped'])
            my_data=sorted_data

            print("up")
        elif 'new' in request.GET:
            # for item in my_data:
            #   if item['price'] is not None:
            #       if item['price']>1000 :
            #        data.append(item)
                 
            sorted_data = sorted(my_data, key=lambda x: x['datescraped'], reverse=True)
            my_data=sorted_data

        

    return redirect(index)

def filter(request):
    global my_data
    populate_data()
    new=[]
    news=[]
    if request.method == 'POST':
        min = request.POST.get('min_price')
        max = request.POST.get('max_price')
        ville = request.POST['state'] 
        
        print(ville)
        if ville:
            for item in my_data:
             if item["state"] and item["state"]==ville:
                new.append(item)
        if min and max:
         for item in news:      
            if item["price"] and item["price"] >=min and item["price"] <=max:
                 news.append(item)
    my_data=new

              
    return redirect(index)
# from django.shortcuts import render
# from django.core.paginator import Paginator, EmptyPage
# from pymongo import MongoClient

# def index(request):
#     # Check if form was submitted
#     if request.method == 'POST':
#         # Get form inputs from request.POST dictionary
#         search_query = request.POST.get('search_query', '').strip()
#         min_price = request.POST.get('min_price')
#         max_price = request.POST.get('max_price')
#         ville = request.POST.get('ville', '').strip()

#         # Connect to database and get data
#         MONGO_URI = 'mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/?retryWrites=true&w=majority'
#         client = MongoClient(MONGO_URI)
#         db = client['AdsScrappers']
#         collection = db['Ads']

#         # Filter data based on form inputs
#         query = {}
#         if search_query:
#             query['$or'] = [
#                 {'title': {'$regex': search_query, '$options': 'i'}},
#                 {'description': {'$regex': search_query, '$options': 'i'}},
#             ]
#         if min_price and max_price:
#             query['price'] = {'$gte': float(min_price), '$lte': float(max_price)}
#         elif min_price:
#             query['price'] = {'$gte': float(min_price)}
#         elif max_price:
#             query['price'] = {'$lte': float(max_price)}
#         if ville:
#             query['ville'] = {'$regex': ville, '$options': 'i'}

#         # Get sorting variable from GET request
#         sort_by = request.GET.get('sort_by', '')

#         # Sort data based on sorting variable
#         if sort_by == 'price_asc':
#             all_data = list(collection.find(query).sort('price', 1))
#         elif sort_by == 'price_desc':
#             all_data = list(collection.find(query).sort('price', -1))
#         elif sort_by == 'date_asc':
#             all_data = list(collection.find(query).sort('dateinstered', 1))
#         elif sort_by == 'date_desc':
#             all_data = list(collection.find(query).sort('dateinstered', -1))
#         else:
#             all_data = list(collection.find(query).sort('dateinstered', -1))

#         # Paginate data
#         page_number = request.GET.get('page', 1)
#         page_number = int(page_number)
#         page_size = 21
#         paginator = Paginator(all_data, page_size)

#         try:
#             data = paginator.page(page_number)
#         except EmptyPage:
#             data = paginator.page(paginator.num_pages)

#         # Render page with filtered and sorted data
#         return render(request, 'index.html', {'data': data})

#     else:
#         # Connect to database and get all data
#         MONGO_URI = 'mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/?retryWrites=true&w=majority'
#         client = MongoClient(MONGO_URI)
#         db = client['AdsScrappers']
#         collection = db['Ads']

#         # Get sorting variable from GET request
#         sort_by = request.GET.get('sort_by', '')

#         # Sort data based on sorting variable
#         if sort_by == 'price_asc':
#             all_data = list(collection.find().sort('price', 1))
#         elif sort_by == 'price_desc':
#             all_data =  list(collection.find().sort('price', -1))
#         elif sort_by == 'date_asc':
#             all_data = list(collection.find().sort('dateinstered', 1))
#         else:
#             all_data = list(collection.find().sort('dateinstered', -1))
#             # Paginate data
#         page_number = request.GET.get('page', 1)
#         page_number = int(page_number)
#         page_size = 21
#         paginator = Paginator(all_data, page_size)

#         try:
#             data = paginator.page(page_number)
#         except EmptyPage:
#             data = paginator.page(paginator.num_pages)

#         # Render page with all data
#         return render(request, 'Home.html', {'data': data})
