from django.db import models

<<<<<<< HEAD
class Product(models.Model):
    SEASON_CHOICES = [
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
        ('Winter', 'Winter'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity_kg = models.FloatField(verbose_name="Current stock (kg)")
    price_per_kg = models.FloatField()
    drying_loss_kg = models.FloatField(default=0)
    seasonal = models.BooleanField(default=False)
    season = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        choices=SEASON_CHOICES
    )

    def __str__(self):
        return self.name

    def update_stock(self, purchased_kg=0, sold_kg=0, drying_loss=0):
        """Automatically updates stock based on purchases, sales, and drying losses."""
        if purchased_kg < 0 or sold_kg < 0 or drying_loss < 0:
            raise ValueError("Quantities cannot be negative!")

        self.quantity_kg += purchased_kg  # Increase stock when buying
        self.quantity_kg -= sold_kg  # Reduce stock when selling
        self.quantity_kg -= drying_loss  # Reduce stock due to drying loss

        if self.quantity_kg < 0:
            raise ValueError("Stock cannot be negative!")
        
        self.save()

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_purchased = models.FloatField()
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity_purchased}kg"
=======
# Create your models here.

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100, choices=[('Coffee', 'Coffee'), ('Maize', 'Maize'), ('Beans', 'Beans')])
    quantity_kg = models.FloatField(default=0)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    drying_loss_kg = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_quantity(self, purchased_kg=0, sold_kg=0, drying_loss_kg=0):
        self.quantity_kg += purchased_kg  # Add purchased quantity
        self.quantity_kg -= (sold_kg + drying_loss_kg)  # Subtract sold & drying loss
        self.save()
>>>>>>> bb7995000adfb11203e87c18f386ac0afe8d6de1
