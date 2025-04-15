from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField # type: ignore

from django.db import models

from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from datetime import datetime
from decimal import Decimal


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
    initial_driedWeight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional
    drying_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    drying_status = models.CharField(max_length=50, choices=[
        ('not_dried', 'Not Dried'),
        ('drying', 'Drying'),
        ('dried', 'Dried')
    ], default='not_dried')
    drying_start_date = models.DateTimeField(default=timezone.now)
    drying_end_date = models.DateTimeField(default=timezone.now)
    product_number = models.PositiveIntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.product_number:
            last_product = Product.objects.order_by('-product_number').first()
            self.product_number = (last_product.product_number + 1) if last_product else 1

        if self.drying_status == 'dried' and self.initial_driedWeight is None:
            self.initial_driedWeight = self.driedWeight  # Capture original dry weight

        super().save(*args, **kwargs)

    @property
    def quantity_purchased(self):
        return self.quantitypurchased.quantityPurchased

    @property
    def is_sold(self):
        return self.driedWeight == 0 and self.drying_status == 'dried'

    def __str__(self):
        return f"{self.categoryName} - {self.drying_status}"
    

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
            last_purchase = Purchase.objects.order_by('-purchase_number').first()
            self.purchase_number = (last_purchase.purchase_number + 1) if last_purchase else 1
        super().save(*args, **kwargs)

    def totalBuyingPrice(self):
        return self.quantityPurchased * self.buyingPrice

    def total_expenses(self):
         drying_total = Decimal('0.00')
         selling_total = Decimal('0.00')
         seen_sales = set()

         products = Product.objects.filter(quantitypurchased=self, drying_status='dried')

         for product in products:
             drying_total += product.drying_expenses or Decimal('0.00')
 
             for detail in product.sale_details.select_related('sale'):
                 sale = detail.sale
                 if sale and sale.id not in seen_sales:
                        print(f"DEBUG - Sale ID: {sale.id}, Selling Expenses: {sale.selling_expenses}")
                        selling_total += sale.selling_expenses or Decimal('0.00')
                        seen_sales.add(sale.id)

         return (self.buying_expenses or Decimal('0.00')) + drying_total + selling_total



    def __str__(self):
        return f"{self.quantityPurchased} kg"


    
class Sale(models.Model):
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    sale_date = models.DateField(default=timezone.now)
    customerName = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantitySold = models.PositiveIntegerField()
    sellingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    selling_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_number = models.PositiveIntegerField(unique=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.sale_number:
            last_sale = Sale.objects.order_by('-sale_number').first()
            self.sale_number = (last_sale.sale_number + 1) if last_sale else 1

        super().save(*args, **kwargs)

        if is_new:
            self.allocate_products_to_sale()

    def allocate_products_to_sale(self):
        """
        Deduct quantitySold from dried Product entries and create SaleDetail entries.
        No longer splits selling expenses per unit — handled as a fixed value per sale.
        """
        with transaction.atomic():
            dried_products = Product.objects.filter(
                categoryName=self.categoryName,
                drying_status='dried',
                driedWeight__gt=0
            ).order_by('drying_end_date')

            remaining = self.quantitySold

            for product in dried_products:
                available = product.driedWeight

                if available >= remaining:
                    SaleDetail.objects.create(
                        sale=self,
                        product=product,
                        quantity=remaining
                    )
                    product.driedWeight -= remaining
                    product.save()
                    break
                else:
                    SaleDetail.objects.create(
                        sale=self,
                        product=product,
                        quantity=available
                    )
                    product.driedWeight = 0
                    product.save()
                    remaining -= available

            if remaining > 0:
                raise ValidationError("Not enough dried weight available for this sale.")

    @property
    def totalSellingPrice(self):
        return self.quantitySold * self.sellingPrice
     
    @property
    def totalBuyingPrice(self):
        return self.purchase.totalBuyingPrice() if self.purchase else Decimal('0.00')
    
    @property
    def total_expenses(self):
        """
        Sum up all expenses related to this sale from its SaleDetails.
        """
        return sum(
            detail.allocated_buying_expense +
            detail.allocated_drying_expense +
            detail.allocated_selling_expense
            for detail in self.details.all()
        )

    @property
    def total_profit_or_loss(self):
        total_cost = self.total_expenses
        total_revenue = self.totalSellingPrice
        return total_revenue - total_cost

    @property
    def total_profit(self):
        # Profit is the positive result of profit_or_loss
        return self.total_profit_or_loss if self.total_profit_or_loss > 0 else 0

    @property
    def total_loss(self):
        # Loss is the negative result of profit_or_loss
        return abs(self.total_profit_or_loss) if self.total_profit_or_loss < 0 else 0

    @classmethod
    def totalSalesByDate(cls, target_date):
        sales = cls.objects.filter(sale_date=target_date)
        return sum(sale.totalSellingPrice for sale in sales)

    def __str__(self):
        return f"Sale of {self.quantitySold} {self.categoryName} to {self.customerName} on {self.sale_date}"

    



class SaleDetail(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sale_details')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def allocated_buying_expense(self):
       purchase = self.product.quantitypurchased

       return purchase.buying_expenses or Decimal('0.00') if purchase else Decimal('0.00')

    @property
    def allocated_drying_expense(self):
        return self.product.drying_expenses or Decimal('0.00')

    @property
    def allocated_selling_expense(self):
        return self.sale.selling_expenses or Decimal('0.00')

    @property
    def total_buying_price(self):
        purchase = self.product.quantitypurchased

        if purchase:
            return purchase.quantityPurchased * purchase.buyingPrice
        return Decimal('0.00')

    @property
    def total_selling_price(self):
        return self.quantity * self.sale.sellingPrice

    @property
    def profit_or_loss(self):
        total_costs = (
            self.total_buying_price +
            self.allocated_buying_expense +
            self.allocated_drying_expense +
            self.allocated_selling_expense
        )
        return self.total_selling_price - total_costs



    

    


    