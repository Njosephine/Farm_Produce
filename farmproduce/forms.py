from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
<<<<<<< HEAD
        fields = ['name', 'category', 'quantity_kg', 'price_per_kg', 'drying_loss_kg', 'seasonal', 'season']

class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity_purchased = forms.FloatField()
    total_cost = forms.FloatField()

=======
        fields = ['name', 'category', 'quantity_kg', 'price_per_kg', 'drying_loss_kg']
>>>>>>> bb7995000adfb11203e87c18f386ac0afe8d6de1
