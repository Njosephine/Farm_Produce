from django import forms
from .models import Category, Customer, Product, Purchase, Sale
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    

class Category_Form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryName']


class Customer_Form(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customerName','contact','address']

class Product_Form(forms.ModelForm):
    quantity_purchased = forms.DecimalField(required=False, disabled=True)  

    class Meta:
        model = Product
        fields = ['categoryName','driedWeight', 'drying_expenses', 'drying_status', 'drying_start_date', 'drying_end_date', 'quantity_purchased']


    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

    # Safe check before accessing .purchase
          if self.instance and hasattr(self.instance, 'purchase') and self.instance.purchase:
              self.fields['quantity_purchased'].initial = self.instance.quantity_purchased  

              self.fields['categoryName'].queryset = Category.objects.all()


class Sale_Form(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['categoryName','sale_date','customerName','quantitySold','sellingPrice','selling_expenses']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('categoryName')
        quantity = cleaned_data.get('quantitySold')

        # Check for available dried products in that category
        available_dried = Product.objects.filter(
            categoryName=category,
            drying_status='dried',
            driedWeight__gt=0
        )

        total_available = sum([p.driedWeight for p in available_dried])

        if quantity and total_available < quantity:
            raise forms.ValidationError(
                f"Not enough dried products available in this category. Available: {total_available}, Requested: {quantity}"
            )
       
class Purchase_Form(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['categoryName','purchasedate','supplierName','quantityPurchased','buyingPrice','buying_expenses']