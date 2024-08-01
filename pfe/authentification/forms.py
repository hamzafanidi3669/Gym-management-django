from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=32, required=True)
    email = forms.EmailField(label='Adresse e-mail', required=True)
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label='Nom', max_length=50, required=True)
    last_name = forms.CharField(label='Prénom', max_length=50, required=True)
    country_user = forms.CharField(label='Country', max_length=150, required=False)
    ville_user = forms.CharField(label='City', max_length=150, required=False)
    adress_user = forms.CharField(label='Adresse', max_length=150, required=False)
    phone_user = forms.CharField(label='Numéro de téléphone', required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'adress_user', 'phone_user','ville_user','country_user')

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
        return username

    def clean_phone_user(self):
        phone_number = self.cleaned_data.get('phone_user', '')
        if not phone_number:
            return ''  # If phone number is empty, allow it to be blank

        if len(phone_number) != 10:
            raise ValidationError("Le numéro de téléphone doit contenir exactement 10 chiffres.")
        
        if not phone_number.isdigit():
            raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")

        if CustomUser.objects.filter(phone_user=phone_number).exists():
            raise ValidationError("Ce numéro de téléphone est déjà utilisé. Veuillez en saisir un autre.")

        return phone_number
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 3:
            raise ValidationError("Le prénom doit contenir au moins 3 caractères.")
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 3:
            raise ValidationError("Le nom de famille doit contenir au moins 3 caractères.")
        return last_name
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return password2
    def clean(self):
        cleaned_data = super().clean()
        self.clean_password2()  
        return cleaned_data
