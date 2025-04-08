# from django.urls import path # type: ignore


from django.urls import path 
from dashboard.views import  index_view, logout_view,profile_view,dashboard_view, products_view, purchases_view, sales_view, category_view,customer_view,supplier_view,add_sale_view,export_sales_csv, export_sales_pdf,edit_sale,delete_sale,edit_purchase,delete_purchase,add_purchase_view,export_purchase_csv,export_purchase_pdf,add_product_view

urlpatterns = [
    # path("home/", home_view, name="home"),
    path("", index_view, name="index"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile" ),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('product/', products_view, name='products'),
    path('purchases/', purchases_view, name='purchases'),
    path('sales/', sales_view, name='sales'),
    path('category/', category_view, name='category'),
    path('customer/', customer_view, name='customer'),
    path('supplier/', supplier_view, name='supplier'),
    path('sales/add/', add_sale_view, name='add_sale'),
    path('export_sales_csv/', export_sales_csv, name='export_sales_csv'),
    path('export_sales_pdf/', export_sales_pdf, name='export_sales_pdf'),
    path('sales/edit/<int:id>/', edit_sale, name='edit_sale'),
    path('sales/delete/<int:id>/', delete_sale, name='delete_sale'),
    path('purchases/add/', add_purchase_view, name='add_purchase'),
    path('purchases/edit/<int:id>/', edit_purchase, name='edit_purchase'),
    path('purchases/delete/<int:id>/', delete_purchase, name='delete_purchase'),
    path('export_purchase_csv/', export_purchase_csv, name='export_purchase_csv'),
    path('export_purchase_pdf/', export_purchase_pdf, name='export_purchase_pdf'),
    path('products/add/', add_product_view, name='add_product'),
]






