from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField # type: ignore

from django.db import models

from django.db import transaction
from django.core.exceptions import ValidationError

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="profile.jpeg")
    bio = models.TextField(blank=True, null=True)
   
    def __str__(self):
        return f"{self.user.username}Profile"
    

class Category(models.Model):
    categoryName  = models.CharField(max_length=100)


    def __str__(self):
        return self.categoryName

class Customer(models.Model):
    contact = PhoneNumberField(unique=True) 
    address = models.CharField(max_length=255)
    customerName = models.CharField(max_length=100)


    def __str__(self):
        return self.customerName
    
class Supplier(models.Model):
    contact = PhoneNumberField(unique=True) 
    address = models.CharField(max_length=255)
    supplierName = models.CharField(max_length=100)


    def __str__(self):
        return self.supplierName
class Product(models.Model):
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantitypurchased = models.ForeignKey('Purchase', on_delete=models.CASCADE)
    driedWeight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    drying_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   
    drying_status = models.CharField(max_length=50, choices=[
        ('not_dried', 'Not Dried'),
        ('drying', 'Drying'),
        ('dried', 'Dried')
    ], default='not_dried')
    drying_start_date = models.DateTimeField(default=timezone.now)
    drying_end_date = models.DateTimeField(default=timezone.now)
    product_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"{self.categoryName} - {self.drying_status}"

    @property
    def quantity_purchased(self):
        return self.quantitypurchased.quantityPurchased
    
    @property
    def is_sold(self):
        return self.driedWeight == 0 and self.drying_status == 'dried'
    
  
    
    def save(self, *args, **kwargs):
        if not self.product_number:
            last_product = Product.objects.order_by('-product_number').first()
            self.product_number = (last_product.product_number + 1) if last_product else 1
        super().save(*args, **kwargs)

    
class Sale(models.Model):
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE) 
    sale_date = models.DateField(default=timezone.now) 
    customerName = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    quantitySold = models.PositiveIntegerField() 
    sellingPrice = models.DecimalField(max_digits=10, decimal_places=2) 
    selling_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    sale_number = models.PositiveIntegerField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.sale_number:
            last_sale = Sale.objects.order_by('-sale_number').first()
            self.sale_number = (last_sale.sale_number + 1) if last_sale else 1
        super().save(*args, **kwargs)

    # Deduct quantitySold from dried Product entries
        with transaction.atomic():
            dried_products = Product.objects.filter(
                categoryName=self.categoryName, 
                drying_status='dried', 
                driedWeight__gt=0
            ).order_by('drying_end_date')

        remaining = self.quantitySold
        for product in dried_products:
                if product.driedWeight >= remaining:
                  product.driedWeight -= remaining
                if product.driedWeight == 0:
                    product.is_sold = True
                    product.save()
                    remaining = 0
                    break
                else:
                   remaining -= product.driedWeight
                   product.driedWeight = 0
                   product.is_sold = True
                   product.save()

        if remaining > 0:
            raise ValidationError("Not enough dried weight available for this sale.")

        super().save(*args, **kwargs)

    @property
    def totalSellingPrice(self):
        return self.quantitySold * self.sellingPrice
    

    def __str__(self):
        return f"Sale of {self.quantitySold} {self.categoryName} to {self.customerName} on {self.selloffdate}"
    
class Purchase(models.Model):
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE) 
    purchasedate = models.DateField(default=timezone.now)  
    supplierName = models.ForeignKey(Supplier, on_delete=models.CASCADE) 
    quantityPurchased = models.PositiveIntegerField() 
    buyingPrice = models.DecimalField(max_digits=10, decimal_places=2) 
    buying_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    purchase_number = models.PositiveIntegerField(unique=True)
  
    def save(self, *args, **kwargs):
        if not self.purchase_number:
            last_purchase= Purchase.objects.order_by('-purchase_number').first()
            self.purchase_number = (last_purchase.purchase_number + 1) if last_purchase else 1
        super().save(*args, **kwargs)
    @property
    def totalBuyingPrice(self):
        return self. quantityPurchased * self.buyingPrice

    def __str__(self):
         return f"{self.quantityPurchased} kg"

       
    

    


    