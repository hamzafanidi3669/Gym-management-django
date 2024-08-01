from django.shortcuts import render , redirect , get_object_or_404
from .models import Order,Order_Details,Product,Category,Cart,CartItem , Subscription , UserSubscription , CustomUser 
from .forms import ProductAddForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages

# pdf:
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def admin_check(user):
    return user.is_superuser

def store(request):
    # produits = Product.objects.filter(is_sale=True)
    categories = Category.objects.filter(parent__isnull=True) #les categories parents
    sous_categories_nutrition = Category.objects.filter(parent_id=1) #recuperer les sous categories dyal nutrition
    sous_categories_vetements = Category.objects.filter(parent_id=2)

    if request.user.is_superuser :
        produits = Product.objects.all()  # Tous les produits pour l'admin
    else:
        produits = Product.objects.filter(is_sale=True)  # Seulement les produits en vente pour les autres


    
    authenticated_user = request.user #recuperer le user authentifié
    
    #filtrage:
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price')
    flavor = request.GET.get('flavor')
    brand = request.GET.get('brand')

    if min_price:
        produits = produits.filter(price__gte=min_price) # gte hya greater than or equal 
    if max_price:
        produits = produits.filter(price__lte=max_price)
    if flavor:
        produits = produits.filter(flavor__icontains=flavor)
    if brand:
        produits = produits.filter(brand__icontains=brand)
    # Récupérer les saveurs uniques non vides
    unique_flavors = produits.exclude(flavor__exact='').values_list('flavor', flat=True).distinct()
    unique_brand = produits.values_list('brand', flat=True).distinct()
    return render(request, 'store/store.html', {
        'produits': produits,
        'categories': categories,
        'complement': sous_categories_nutrition,
        'vetements': sous_categories_vetements,
        'min_price': min_price,
        'max_price': max_price,
        'flavor': flavor,
        'brand': brand,
        'unique_flavors': unique_flavors,
        'unique_brand': unique_brand,
        'authenticated_user':authenticated_user
    })



def news_product(request):
    twenty_days_before=timezone.now() - timedelta(days=20) #10 juin 
    # produits=Product.objects.filter(created_at__gte=twenty_days_before , is_sale=True) #ghadi yrecup les produit lli mcreeyin > men 10juin  (9bel 20jours)
    categories = Category.objects.filter(parent__isnull=True) #les parents 3la 9bel mininav
    # return render(request,'store/news_product.html',{'produitsnews':produits,'categories':categories})

    if request.user.is_superuser :
        # produits = Product.objects.all()  # Tous les produits pour l'admin
        produits=Product.objects.filter(created_at__gte=twenty_days_before) #ghadi yrecup les produit lli mcreeyin > men 10juin  (9bel 20jours)

    else:
        produits = Product.objects.filter(created_at__gte=twenty_days_before , is_sale=True)  # Seulement les produits en vente pour les autres

    authenticated_user = request.user



    sous_categories_nutrition = Category.objects.filter(parent_id=1)
    sous_categories_vetements = Category.objects.filter(parent_id=2)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    flavor = request.GET.get('flavor')
    brand = request.GET.get('brand')

    if min_price:
        produits = produits.filter(price__gte=min_price) #greater than or equal 
    if max_price:
        produits = produits.filter(price__lte=max_price)
    if flavor:
        produits = produits.filter(flavor__icontains=flavor)
    if brand:
        produits = produits.filter(brand__icontains=brand)

    # Récupérer les saveurs uniques non vides
    unique_flavors = produits.exclude(flavor__exact='').values_list('flavor', flat=True).distinct()
    unique_brand = produits.values_list('brand', flat=True).distinct()

    return render(request, 'store/news_product.html', {
        'produits': produits,
        'categories': categories,
        'complement': sous_categories_nutrition,
        'vetements': sous_categories_vetements,
        'min_price': min_price,
        'max_price': max_price,
        'flavor': flavor,
        'brand': brand,
        'unique_flavors': unique_flavors,
        'unique_brand': unique_brand,
        'authenticated_user':authenticated_user
    })



@user_passes_test(admin_check, login_url='/')
def addproduct(request):
    authenticated_user = request.user
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Ne sauvegardez pas immédiatement
            
            # Vérifiez si le champ 'brand' est vide
            if not product.brand:
                product.brand = "Autre"  # Remplacez par votre valeur par défaut
            
            product.save()  # Maintenant, sauvegardez le produit
            return redirect('/store/')
    else:
        form = ProductAddForm()
    
    return render(request, 'store/addproduct.html', {
        'form': form, 
        'authenticated_user': authenticated_user
    })

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.filter(parent__isnull=True)  # les parents

    authenticated_user = request.user

    # Vérifier si l'utilisateur est un membre du staff (admin)
    is_admin = authenticated_user.is_superuser

    if category.parent is None:
        # Si c'est une catégorie parent, prendre les sous-catégories
        subcategories = Category.objects.filter(parent=category)
        if request.user.is_superuser:
            produits = Product.objects.filter(category__in=subcategories)
        else:
            produits = Product.objects.filter(category__in=subcategories, is_sale=True)
    else:
        if request.user.is_superuser:
            produits = Product.objects.filter(category=category)
        else:
            produits = Product.objects.filter(category=category, is_sale=True)
    
    # Filtrage par prix
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        produits = produits.filter(price__gte=min_price)
    if max_price:
        produits = produits.filter(price__lte=max_price)

    brand = request.GET.get('brand')
    if brand:
        produits = produits.filter(brand__icontains=brand)

 
    flavor = request.GET.get('flavor')
    if flavor:
        produits = produits.filter(flavor__icontains=flavor)

    # Récupérer les saveurs uniques non vides
    unique_flavors = produits.exclude(flavor__exact='').values_list('flavor', flat=True).distinct()
    unique_brand = produits.values_list('brand', flat=True).distinct()

    return render(request, 'store/category_products.html', {
        'category': category,
        'categories': categories,
        'produits': produits,
        'unique_flavors': unique_flavors,
        'unique_brand': unique_brand,
        'flavor': flavor,
        'brand': brand,
        'authenticated_user': authenticated_user,
        'is_admin': is_admin  
    })

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    categories = Category.objects.filter(parent__isnull=True) #les parents
    authenticated_user = request.user


    return render(request, 'store/cart.html',{'cart':cart,'categories':categories, 'authenticated_user':authenticated_user})




@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)


    if request.method == 'POST':
        quantity=int(request.POST.get('quantity',1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity  
        else:
            cart_item.quantity += quantity
        cart_item.save()
    return redirect('view_cart')


@login_required
def remove_from_cart(request , product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('view_cart')

@login_required
def update_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1)) # 1 par defaut
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('view_cart')







@login_required
def confirm_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    categories = Category.objects.filter(parent__isnull=True)
    authenticated_user = request.user
    
    if cart.items.exists():
        order = Order.objects.create(user=request.user, status_commande=False)
        
        for cart_item in cart.items.all():
            product = cart_item.product
            quantity = cart_item.quantity

            if product.quantity_stock >= quantity:
                Order_Details.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                
                # fash kayconfirmi l order , darori khask qte tn9oss menha sh7al khda
                product.quantity_stock -= quantity
                product.save()
            else:
                #ila makansh qte 
                order.delete()  # Annuler la commande
                messages.error(request, f"Pas assez de stock pour {product.name}. Commande annulée.")
                return redirect('view_cart')
        
        # khwi lpanier
        cart.items.all().delete()
        
        messages.success(request, "Commande confirmée avec succès!")
        return render(request, 'store/confirm_order.html', {
            'order': order,
            'categories': categories,
            'authenticated_user': authenticated_user
        })
    
    messages.info(request, "Votre panier est vide.")
    return redirect('view_cart')








# pdf:

@login_required
def generate_pdf(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    html_string = render_to_string('store/invoice.html', {'order': order})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=order_{order.id}.pdf'
    
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response



def produit(request,produit_id):
    categories = Category.objects.filter(parent__isnull=True) #les parents 3la 9bel mininav
    produit=get_object_or_404(Product,id=produit_id)

    authenticated_user = request.user

    produits = Product.objects.exclude(id=produit.id)[:4] #kanrecuperer 4 dles elements wdert exclude bash mannakhudsh hadak l'element lli deja ana dakhl l3ndo 
    return render(request,'store/product.html',{'product':produit,'categories':categories,'produits':produits, 'authenticated_user':authenticated_user})


def pack(request,packid):
    authenticated_user = request.user
    sub=get_object_or_404(Subscription , id=packid)
    now = timezone.now().date() 

    return render(request,"store/packs/pack.html", {'authenticated_user':authenticated_user , 'sub':sub,'now':now})



def allpacks(request):
    authenticated_user = request.user
    allsub=Subscription.objects.filter(is_active__isnull=False)
    return render(request,"store/packs/allpacks.html", {'authenticated_user':authenticated_user , 'allsub':allsub})




def form_pack_validate(request):
    if request.method == 'POST':
        authenticated_user = request.user
        now = timezone.now().date()
        user=get_object_or_404(CustomUser , id=authenticated_user.id)
        
        sub_id = request.POST.get('subtype')
        if not sub_id:
            messages.error(request, "Le type d'abonnement est obligatoire.")
            return redirect('form_page')
        
        try:
            sub = get_object_or_404(Subscription, id=sub_id)
        except:
            messages.error(request, "Type d'abonnement invalide.")
            return redirect('form_page')
        
        active_subscription = UserSubscription.objects.filter(
            user=authenticated_user,
            end_date__gte=now
        ).exists()
        
        if active_subscription:
            messages.error(request, "Vous avez déjà un abonnement actif.")
            return redirect('store')
        
        user.type_user = "membre"
        user.save()
        
        UserSubscription.objects.create(
            user=authenticated_user,
            subscription=sub,
            start_date=now,
            end_date=now + timedelta(days=365)
        )
        
        messages.success(request, "Votre abonnement a été créé avec succès.")
        return redirect('store')
    
    return redirect('store')


@user_passes_test(admin_check, login_url='/')
def delete_product(request):  
    if request.method == 'POST':
        productid = request.POST.get('productid')
        try:
            product = get_object_or_404(Product, id=productid)
            product.delete()
            messages.success(request, f"Le produit '{product.name}' a été supprimé avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression du produit : {str(e)}")
    else:
        messages.error(request, "Méthode non autorisée pour supprimer le produit.")
    return redirect('store')

@user_passes_test(admin_check, login_url='/')
def modify_product(request, productid):
    product = get_object_or_404(Product, id=productid)
    authenticated_user = request.user
    categories = Category.objects.filter(parent__isnull=False)
    errors = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        # price = request.POST.get('price')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        brand = request.POST.get('brand')
        flavor = request.POST.get('flavor')
        sale_price = request.POST.get('sale_price')
        is_sale = 'is_sale' in request.POST
        qte_stock = request.POST.get('quantity_stock')
        
        if not name:
            errors['name'] = 'Le nom du produit est requis.'
       
        if not description:
            errors['description'] = 'La description du produit est requise.'
        if image and not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            errors['image'] = 'Le fichier image doit être au format PNG, JPG ou JPEG.'
        if not brand:
            errors['brand'] = 'La marque est requise.'
       
        if not sale_price or not sale_price.replace('.', '', 1).isdigit():
            errors['sale_price'] = 'Le prix de vente est requis et doit être un nombre.'
        
        if not errors:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                errors['category'] = "La catégorie sélectionnée n'existe pas."

            if not errors:
                product.name = name
                product.category = category
                product.description = description
                if image:
                    product.image = image
                product.brand = brand
                product.flavor = flavor
                product.sale_price = float(sale_price)
                product.is_sale = is_sale
                product.quantity_stock = qte_stock
                product.save()
                
                messages.success(request, 'Le produit a été mis à jour avec succès.')
                return redirect('store')

    context = {
        'product': product,
        'categories': categories,
        'authenticated_user': authenticated_user,
        'errors': errors
    }
    return render(request, 'store/modify_product.html', context)

