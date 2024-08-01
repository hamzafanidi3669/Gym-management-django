from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, verbose_name="Prénom" , default="")  # Champ pour le prénom de l'utilisateur
    last_name = models.CharField(max_length=150, verbose_name="Nom de famille",default="")  # Champ pour le nom de famille de l'utilisateur
    phone_user=models.CharField(max_length=10,verbose_name="Telephone", default="",blank=True) #blank true z3ma optionnal
    adress_user=models.CharField(max_length=150,verbose_name="Adresse" , default="",blank=True)
    country_user=models.CharField(max_length=150,verbose_name="Country" , default="",blank=True)
    ville_user=models.CharField(max_length=150,verbose_name="Ville" , default="",blank=True)
    # membre howa lli 3ndo pack
    type_user = models.CharField(max_length=20, choices=[
        ('admin', 'Administrateur'),
        ('moderateur', 'Modérateur'),
        ('membre', 'Membre'),
        ('client', 'Client'),
        ('visiteur', 'Visiteur'),
    ], default='client')
    username = models.CharField(max_length=150, unique=True, verbose_name="Nom d'utilisateur")  # Identifiant unique pour la connexion
    email = models.EmailField(max_length=255, unique=True, verbose_name="Adresse e-mail")  # Adresse e-mail de l'utilisateur
    password = models.CharField(max_length=128, verbose_name="Mot de passe")  # Mot de passe de l'utilisateur
    is_superuser = models.BooleanField(default=False, verbose_name="Superutilisateur")  # Statut de superutilisateur
    is_staff = models.BooleanField(default=False, verbose_name="Membre du personnel")  # Statut de membre du personnel
    is_active = models.BooleanField(default=True, verbose_name="Utilisateur actif")  # bash n9der nbannil users
    last_login = models.DateTimeField(verbose_name="Dernière connexion",null=True)  # Date et heure de la dernière connexion
    date_joined = models.DateTimeField(verbose_name="Date d'inscription",null=True,auto_now_add=True)  # Date et heure d'inscription de l'utilisateur
    #  profile :
    photo_profil=models.ImageField(upload_to='uploads/profile/photo_profil',null=True,default="uploads/photo_profil/photo_profil_default.jpg")
    photo_couverture=models.ImageField(upload_to='uploads/profile/photo_couverture',null=True, default="uploads/photo_couverture/couv2.jpg")
    bio_user=models.CharField(max_length=150,verbose_name="Bio" , default="",blank=True)
    # birthdate=models.DateField(null=True , verbose_name="Date de naissance")
    is_verified=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"  
    def get_profile_pic_post_id(self):
        profile_pic_post = self.posts.filter(postimage=self.photo_profil).first()
        return profile_pic_post.id if profile_pic_post else None
    def get_couverture_pic_post_id(self):
        couverture_pic_post = self.posts.filter(postimage=self.photo_couverture).first()
        return couverture_pic_post.id if couverture_pic_post else None


