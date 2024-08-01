from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Import your custom user model
from .forms import RegistrationForm
# Create your views here.
def logine(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Vérifiez d'abord si l'utilisateur existe
        try:
            user = CustomUser.objects.get(username=username)
            if not user.is_active:
                messages.error(request, "Your account was banned")
                return redirect('login')
        except CustomUser.DoesNotExist:
            pass  # L'utilisateur n'existe pas, on continue vers l'authentification

        user = authenticate(request, username=username, password=password) #kiberifie wash howa hadak 
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Email ou mot de passe incorrect!")
            return redirect('login')
    else:
        return render(request, "authentification/login.html")
    

@login_required
def logoute(request):
    logout(request)
    messages.success(request,("logout successfully"))
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Récupérer les données du formulaire
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']  # Utiliser password1 qui est le champ du formulaire
            # Créer un nouvel utilisateur CustomUser
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            # Remplir les champs supplémentaires
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_user = form.cleaned_data['phone_user']
            user.country_user = form.cleaned_data['country_user']
            user.ville_user = form.cleaned_data['ville_user']
            user.adress_user = form.cleaned_data['adress_user']
            user.type_user = 'client'  # Vous pouvez ajuster cela selon vos besoins
            # Sauvegarder l'utilisateur avec les champs supplémentaires
            user.save()
            # Connexion automatique de l'utilisateur après l'inscription
            login(request, user)
            # Redirection vers la page de succès
            return redirect('/')
        else:
            # Affiche les erreurs s'il y en a
            context = {'form': form}
            return render(request, "authentification/register.html", context)
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, "authentification/register.html", context)
