from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
# from django.core.cache import cache
# import pymongo
# from django.core.cache.backends.memcached import PyMemcacheCache
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from pymongo import MongoClient, ASCENDING
from django.conf import settings
from pymemcache.client.base import Client



# cache = Client(('localhost', 11211))
# cache.set('key', 'value', noreply=False, expire=3600, min_compress_len=1024*1024)


def ImmoApp(request):
  template = loader.get_template('Home.html')
  return HttpResponse(template.render())


# def index(request):
#     # Check if the data is cached
#     print("************************************************")
#     cached_data = cache.get('my_data')
    
#     print(cached_data)
#     if cached_data is not None:
#         # Use the cached data
#         data = cached_data
#     else:
#         # Connect to MongoDB Atlas and retrieve data
#         MONGO_URI = 'mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/?retryWrites=true&w=majority'
#         client = pymongo.MongoClient(MONGO_URI)
#         db = client['AdsScrappers']
#         collection = db['Ads']
#         data = list(collection.find())

#         # # Cache the data for 1 hour
#         cache.set('my_data', data, 3600)

#     # Pass the data to the template
#         return render(request, 'Home.html', {'data': data})


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def index(request):
    # Check if the data is cached
    cached_data = cache.get('my_data')
    if cached_data is not None:
        # Use the cached data
        data = cached_data
    else:
        # Connect to MongoDB Atlas and retrieve data
        MONGO_URI = 'mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(MONGO_URI)
        db = client['AdsScrappers']
        collection = db['Ads']

        # Get the total number of documents
        count = collection.count_documents({})

        # Set the number of documents to retrieve per page
        page_size = 100

        # Retrieve each page of documents and cache it separately
        data = []
        for i in range(0, count, page_size):
            page_data = list(collection.find().skip(i).limit(page_size).sort('date', ASCENDING))
            cache.set(f'my_data_{i}', page_data, CACHE_TTL)
            data += page_data

        # Cache the complete data for 1 hour
        cache.set('my_data', data, CACHE_TTL)

    # Pass the data to the template
    return render(request, 'Home.html', {'data': data})
