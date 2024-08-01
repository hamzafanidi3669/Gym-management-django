from django.urls import path
from . import views

urlpatterns = [
    path('login', views.logine , name="login"),
    path('logout', views.logoute , name="logout"),
    # path('test', views.test , name="test"),
    path('register', views.register , name="register"),
]