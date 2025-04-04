from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Customer, Profile
from .forms import Category_Form, Customer_Form


def index_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard")
            else:
               form.add_error(None, 'Invalid username or password') 
       

    return render(request, "accounts/auth.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index") 



# def home_view(request):
#     return render(request, "dashboard/home.html")

@login_required
def profile_view(request):
    profile, created =Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

def products_view(request):
    return render(request, 'dashboard/products.html')

def purchases_view(request):
    return render(request, 'dashboard/purchase.html')

def sales_view(request):
    return render(request, 'dashboard/sales.html')


def supplier_view(request):
    return render(request, 'dashboard/supplier.html')

def customer_view(request):
    return render(request, 'dashboard/customer.html')

#categories
def category_view(request):
    form = Category_Form()  
    categories = Category.objects.all()


    if request.method == 'POST':
        form = Category_Form(request.POST)  #
        if form.is_valid():
            form.save()
            return redirect('category')  

    return render(request, "dashboard/category.html", {"form": form, "categories": categories}) 

#customer
def customer_view(request):
    form = Customer_Form()  
    customers = Customer.objects.all()


    if request.method == 'POST':
        form = Customer_Form(request.POST)  #
        if form.is_valid():
            form.save()
            return redirect('category')  

    return render(request, "dashboard/category.html", {"form": form, "customers": customers})

