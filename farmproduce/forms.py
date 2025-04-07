from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity_kg', 'price_per_kg', 'drying_loss_kg', 'seasonal', 'season']

class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity_purchased = forms.FloatField()
    total_cost = forms.FloatField()

