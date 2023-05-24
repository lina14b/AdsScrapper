# -*- coding: utf-8 -*-
import json
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.urls import reverse
from pymongo import MongoClient
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
import pandas as pd
sys.path.append('C:/Users/Lina/Desktop/AdsScrapper/AdsScrapper/AdsScrapper/AdsScrapper')
from bienImmobilier import BienImmobilier
from user import User
from Ads_recherche_text import Recherche
from datetime import timedelta



def ImmoApp(request):
  template = loader.get_template('Home.html')
  return HttpResponse(template.render())



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
user=User()
my_data = []
my_dataBU = []
typeB= ['Villa','Appartement','Terrain','Maison','Commercial','Autre','Dépôt','Bureau']
ville=[]
state= ['Ariana','Beja','Ben Arous','Bizerte','Gabes','Gafsa','Jendouba','Kairouan','Kasserine','Kebili','Kef', 'Mahdia','Manouba','Medenine','Monastir','Nabeul','Sfax','Sidi Bouzid','Siliana','Sousse','Tataouine','Tozeur','Tunis','Zaghouan']
r=Recherche()
msg=""
i=0
my_data = cache.get('my_data')

def populate_data():
    b=BienImmobilier()
    global my_data
    global my_dataBU
    global ville
    
    my_data = b.readAll()
    my_dataBU=my_data
    ville=b.getvilles(my_dataBU)
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
        global msg
        global i
        if i==1:
           i=0
        else:
           msg=""
        global my_data
        author_id = request.user.id
        authorname = request.user.username
        print("\n*******")
        print("\n*******",author_id)
        res=None
        search=""
        if request.method == 'POST':
         search = request.POST.get('search')
         res=r.search_text(search)
         search="Results for "+search+":"
         
          
        if not res:res=my_data
        my_data=res
        


        if not my_data:
            print("populate data")
            populate_data()
            cache.set('my_data', my_data,3600)
        page_number = request.GET.get('page', 1)
        page_number = int(page_number)
        
        data=[]
    
        
        page_size = 21

        all_data = my_data

        paginator = Paginator(all_data, page_size)

        try:
            data = paginator.page(page_number)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

      

        return render(request, 'Home.html', {'data': data, 'page': page_number,'state':state,'authorid':author_id,'authorname':authorname,'search':search,'msg':msg,'ville':json.dumps(ville) ,'typeB':typeB})

def sort(request):
    global my_data
    
    b=BienImmobilier()
    data=[]
    if  my_data:
        if 'up-arrow' in request.GET:
            ###
            my_data=b.sortprice(my_data,"up")
            
        elif 'down-arrow' in request.GET:
            my_data=b.sortprice(my_data,"down")
            
        if 'old' in request.GET:
            my_data=b.sortdate(my_data,"up")
            
        elif 'new' in request.GET:
            my_data=b.sortdate(my_data,"down")
      
    return redirect(index)

def filter(request):
    global my_data
    global msg
    my_data=my_dataBU
    min = None
    max = None
    state = None
    ville = None
    typeb = None
    b=BienImmobilier()
    new=[]
    if request.method == 'POST':
        min = request.POST.get('min_price')
        max = request.POST.get('max_price')
        state = request.POST.get('state')
        ville = request.POST.get('ville')
        typeb = request.POST.get('typeB')
        print(request.POST)
        print(ville,state,min,max,typeb)
        new=b.filterdata(my_data,ville,state,min,max,typeb)
    print("len",len(new))
    if(len(new)==0):
       new=my_dataBU
       msg="No Ads found"
       global i
       i=1

    my_data=new
        # print("***-----------------------******")
        # print(request.POST)
        
        # print("++++++",state)
        # if state:
         
        #  if min and max:
        #   print(min,max)
        #   for item in my_data:      
        #     if item["state"] and item["state"]==state and item["price"] and item["price"] >=int(min) and item["price"] <=int(max):
        #          new.append(item)
        #  else:
        #     for item in my_data:
        #      if item["state"] and item["state"]==state:
        #         new.append(item)
 
    

              
    return redirect(index)

def Clearfilter(request):
    global my_data
    
    my_data=my_dataBU
              
    return redirect(index)


def details(request):
   author_id = request.user.id
   authorname = request.user.username
   print(user.email)
   b=BienImmobilier()
   id = request.GET.get('item')
   print(id)
   b.ReadbyId(id)
   print(b.url)
   user.readone(request.user.id)
   print(user.savedIds)
   saved=id in user.savedIds
     
   return render(request, 'item.html', {'item': b,'user':user,'saved':saved})

def profile(request):
   global user 
   print("----------------------------------------")
   if request.method == 'POST':
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        min_surf = request.POST.get('min_surf')
        max_surf = request.POST.get('max_surf')
        villes = request.POST.get('ville')
        states = request.POST['state'] 
        typ=request.POST['typeb'] 
        print(typ)

        test=user.readone(request.user.id)

        u=User(request.user.id,request.user.email,min_price,max_price,min_surf,max_surf,states,villes,typ,user.saved,user.savedIds)
        
        if test:u.update()
        else:u.save()
   
   if not request.user.is_authenticated:
      return redirect('login_user')
   else: 
      user.readone(request.user.id)
      print("______",user.state)
      print(user.ville,user.typeb)
      print(ville)
      
   

   return render(request,"profile.html", {'state':state,'user':user,'ville':ville,'typeB':typeB})

def removesaved(request):
   global user 
   user.readone(request.user.id)
   user.id=request.user.id
   user.RemoveSaved(user,request.GET.get('item'))
   return redirect('profile')

def addtosaved(request):
   global user 
   user.readone(request.user.id)
   user.id=request.user.id
   user.AddSaved(user,request.GET.get('item'))
   id="?item="+request.GET.get('item')
   return redirect(reverse('details') +id)

def userauth(request):
  return render(request,"profile.html")

def register(request):
 
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password==confirm_password:
      if User.objects.filter(username=username).exists():
        messages.info(request,'Username is already taken')
        return redirect('register')
  
      else:
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return redirect('login_user')
      
  else:
    return render(request, "register.html")
    
def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username,password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('profile')
    else: 
      messages.info(request, 'Invalid Username or Password')
      return redirect('login_user')
  
  else:
   return render(request,"login.html")


def logout_user(request):
  auth.logout(request)
  return render(request,"login.html")

def stats(request):
  return render(request,"statistique.html")
  

