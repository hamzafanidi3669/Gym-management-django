from django.urls import path
from . import views 

urlpatterns = [
    path('' , views.store , name="store"),
    path('addproduct' , views.addproduct , name="addproduct"),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    
    # panier:
    path('view_cart', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Corrected
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:product_id>/', views.update_cart_item, name='update_cart_item'),

    path('confirm_order/', views.confirm_order, name='confirm_order'),


# pdf
    path('generate_pdf/<int:order_id>/', views.generate_pdf, name='generate_pdf'),


    path('produit/<int:produit_id>/', views.produit, name='produit'),


    path('product_news', views.news_product, name='news_product'),




    path('pack/<int:packid>/', views.pack , name='pack'),
    path('form_pack_validate/', views.form_pack_validate,name='form_pack_validate'),
    path('allpacks/', views.allpacks,name='allpacks'),



    path('delete_product/', views.delete_product,name='delete_product'),
    
    path('modify_product/<int:productid>/', views.modify_product,name='modify_product'),

]
