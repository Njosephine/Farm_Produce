from django.contrib import admin
from .models import Category, Customer
# Register your models here.


# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryName') 

#Register Customer model

@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'customerName','contact','address') 
