from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .models import Category


class ProductAddForm(forms.ModelForm):
    """
    Formulaire d'inscription étendu avec des champs supplémentaires.
    """

    # les valeurs par defaut kikono f models mashi hlforms
    #upload to makkaddarsh hna
    name = forms.CharField(label="Nom De Produits", max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'inputs_addproduct', 'placeholder': 'Nom de Produit'}))
    price = forms.DecimalField(label='Prix de produit',decimal_places=2,max_digits=6, required=True,  widget=forms.NumberInput(attrs={'class': 'inputs_addproduct', 'placeholder': 'Prix de Produit'}))
    # ghadi nrecuperi gher les sous category 7tash sous category ra aslan mrbota bcateg parent 
    category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=False),empty_label='Select une catégorie', label='Categorie', required=True ,  widget=forms.Select(attrs={'class': 'inputs_addproduct'}))# ha lforeign key kifsh  
    description = forms.CharField(label='Description De produit', required=True,  widget=forms.Textarea(attrs={'class': 'inputs_addproduct input_description', 'placeholder': 'Description produit'}))
    image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'inputs_addproduct'})
    )
    is_sale = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'inputs_addproduct_boolean'}))
    sale_price=forms.DecimalField(decimal_places=2,max_digits=6, widget=forms.TextInput(attrs={'class': 'inputs_addproduct', 'placeholder': 'Sale_price'})) 

    flavor = forms.CharField(label="Flavor De Produit", max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'inputs_addproduct', 'placeholder': 'Flaveur de Produit'}))
    brand = forms.CharField(label="Brand De Produits", max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'inputs_addproduct', 'placeholder': 'Brand de Produit'}))

    # brand = forms.CharField(label="Brand De Produits",max_length=50,required=False, initial='NomDeMarqueParDefaut',  widget=forms.TextInput(attrs={'class': 'inputs_addproduct','placeholder': 'Brand de Produit'}))

    quantity_stock = forms.CharField(label="Quantity Stock", max_length=50, required=False, widget=forms.NumberInput(attrs={'class': 'inputs_addproduct', 'placeholder': 'Quantity Stock'}))
  
    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'description', 'image', 'is_sale', 'sale_price','flavor','brand', 'quantity_stock')


   