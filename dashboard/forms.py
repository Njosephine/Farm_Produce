from django import forms
from .models import Category, Customer
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