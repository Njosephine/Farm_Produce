
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
<<<<<<< HEAD
    path('purchase/<int:product_id>/', views.purchase_product, name='purchase_product'),    
]
=======
]
>>>>>>> bb7995000adfb11203e87c18f386ac0afe8d6de1
