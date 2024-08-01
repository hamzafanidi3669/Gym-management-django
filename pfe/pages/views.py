from django.shortcuts import render 
from store.models import Subscription
# Create your views here.
def home(request):
    authenticated_user = request.user
    subs=Subscription.objects.all()
    return render(request,"pages/home.html",{'authenticated_user':authenticated_user ,'subs':subs})

def about(request):
    authenticated_user = request.user
    return render(request,"pages/about.html", {'authenticated_user':authenticated_user})


def contact(request):
    authenticated_user = request.user
    return render(request,"pages/contact.html", {'authenticated_user':authenticated_user})


