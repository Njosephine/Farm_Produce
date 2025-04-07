from django.db import models

# Create your models here.

from django.db import models


from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity_kg = models.FloatField()  # Current stock
    price_per_kg = models.FloatField()
    drying_loss_kg = models.FloatField(default=0)

    seasonal = models.BooleanField(default=False)
    season = models.CharField(max_length=50, blank=True, null=True)

    def update_stock(self, purchased_kg=0, sold_kg=0, drying_loss=0):
        """
        Automatically updates stock based on purchases, sales, and drying losses.
        """
        if purchased_kg < 0 or sold_kg < 0 or drying_loss < 0:
            raise ValueError("Quantities cannot be negative!")

        self.quantity_kg += purchased_kg  # Increase stock when buying
        self.quantity_kg -= sold_kg  # Reduce stock when selling
        self.quantity_kg -= drying_loss  # Reduce stock due to drying loss

        if self.quantity_kg < 0:  # Ensure stock doesn't go negative
            raise ValueError("Stock cannot be negative!")

        self.save()



class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity_kg = models.FloatField()
    price_per_kg = models.FloatField()
    seasonal = models.BooleanField(default=False)
    season = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # Add category field
    drying_loss_kg = models.FloatField(default=0)  # Add drying loss field

    def __str__(self):
        return self.name


    # Add a new model for transactions
class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_purchased = models.FloatField()
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity_purchased}kg"

