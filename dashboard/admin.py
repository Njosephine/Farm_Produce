from django.contrib import admin
from .models import Category, Customer, Product, Purchase, Sale, Supplier
# Register your models here.


# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryName') 

#Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customerName','contact','address') 


#Register Supplier model
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplierName','contact','address') 

#Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','categoryName','quantityPurchased','driedWeight','drying_expenses','drying_status','drying_start_date','drying_end_date') 

    def quantityPurchased(self, obj):
        return obj.quantity_purchased
    quantityPurchased.admin_order_field = 'purchase__quantityPurchased'
    quantityPurchased.short_description = 'Quantity Purchased'


#Register model
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id','categoryName','sale_date','customerName','quantitySold','sellingPrice','selling_expenses') 


#Register model
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id','categoryName','purchasedate','supplierName','quantityPurchased','buyingPrice','buying_expenses')