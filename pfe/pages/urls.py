from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home,name='homeglobal'),
    path('about', views.about,name='about'),
    path('contact', views.contact,name='contact'),

   
]