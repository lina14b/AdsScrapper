from django.urls import path
from django.contrib.auth.models import User,auth
from . import views

urlpatterns = [
    path('ImmoApp/', views.ImmoApp, name='ImmoApp'),
    path('',views.userauth,name='userauth'),
    path('register/', views.register, name='register'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
]