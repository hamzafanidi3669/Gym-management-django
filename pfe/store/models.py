from django.db import models
from authentification.models import CustomUser
from django.utils import timezone

class Category(models.Model):
    name=models.CharField(max_length=50)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subcategories')
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(decimal_places=2,max_digits=6,default=0) #max_digits 6 hya = 9999.99 
    quantity_stock = models.PositiveIntegerField(default=1)
    category=models.ForeignKey(Category,on_delete=models.CASCADE , default=1)
    description=models.CharField(max_length=254,default='',blank=True,null=True)
    image=models.ImageField(upload_to='uploads/product/')
    created_at=models.DateTimeField(default=timezone.now)
    brand = models.CharField(max_length=50,default='autre')  # Champ pour la marque
    flavor = models.CharField(max_length=50,default='vanille')  # Champ pour le parfum
    is_sale=models.BooleanField(default=False) # possible nder soldout 
    sale_price=models.DecimalField(decimal_places=2,max_digits=6,default=0) #ila bghet ndir soldes 

    def __str__(self):
        return self.name  
class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    status_commande=models.BooleanField(default=False) #drt default false tanconfirmiwha hna
    def __str__(self):
        return f"Commande {self.id} de {self.user.username}"
    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.order_details_set.all())
    
class Order_Details(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"commande numero {self.order} de produit numero {self.product}"
    
    def get_total_price(self):
        return self.product.price * self.quantity
# Cart 
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart of {self.user}'
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
#Cart_product
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_total_price(self):
        return self.product.price * self.quantity

class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('BRONZE', 'Bronze'),
        ('GOLD', 'Gold'),
        ('PREMIUM', 'Premium'),
    ]

    choice_hours = [
        ('normal access', '06:00-22:00'),
        ('illimited access', '24h'),
    ]
    type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES)
    duration = models.CharField(max_length=10, default='Annuel')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)    
    # Si un utilisateur peut avoir plusieurs abonnements actifs en même temps
    # Caractéristiques spécifiques à chaque type d'abonnement
    access_hours = models.CharField(max_length=100 , choices=choice_hours)  # Par exemple: "06:00-22:00" ou "Illimité"
    coach_sessions = models.IntegerField(default=0)
    class_access = models.BooleanField(default=False)
    friend_invites = models.IntegerField(default=0)
    # shop_discount = models.IntegerField(default=0)  # apres je vais ajouter ca ap
    def __str__(self):
        return f"{self.get_type_display()} - {self.get_duration_display()}"
    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_subscriptions')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='user_subscriptions')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user.username} - {self.subscription.get_type_display()} ({self.start_date} to {self.end_date})"
    def is_current(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.is_active
    class Meta:
        verbose_name = "Abonnement Utilisateur"
        verbose_name_plural = "Abonnements Utilisateurs"
        unique_together = ['user', 'subscription', 'start_date']  # Empêche les doublons

