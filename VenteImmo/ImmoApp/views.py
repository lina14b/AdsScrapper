from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
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

def userauth(request):
  return render(request,"user.html")

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
      return redirect('userauth')
    else: 
      messages.info(request, 'Invalid Username or Password')
      return redirect('login_user')
  
  else:
   return render(request,"login.html")


def logout_user(request):
  auth.logout(request)
  return redirect('userauth')

  

