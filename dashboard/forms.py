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
    class Meta:
        model = Product
        fields = ['categoryName', 'quantitypurchased', 'drying_status', 'drying_start_date', 'driedWeight', 'drying_end_date', 'drying_expenses']
        widgets = {
            'drying_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'drying_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoryName'].queryset = Category.objects.all()
        self.fields['quantitypurchased'].queryset = Purchase.objects.all()

        self.fields['driedWeight'].required = False
        self.fields['drying_end_date'].required = False
        self.fields['drying_expenses'].required = False

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('drying_status')

        if status == 'dried':
            if not cleaned_data.get('driedWeight'):
                self.add_error('driedWeight', 'This field is required when drying status is dried.')
            if not cleaned_data.get('drying_end_date'):
                self.add_error('drying_end_date', 'This field is required when drying status is dried.')
            if not cleaned_data.get('drying_expenses'):
                self.add_error('drying_expenses', 'This field is required when drying status is dried.')

        return cleaned_data




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
        widgets = {
            'purchasedate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
