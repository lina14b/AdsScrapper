from django.urls import path
from . import views

urlpatterns = [
    path('ImmoApp/', views.ImmoApp, name='ImmoApp'),
]