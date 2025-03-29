from django.db import models

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
