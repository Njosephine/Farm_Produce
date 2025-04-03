from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile


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

def category_view(request):
    return render(request, 'dashboard/category.html')

def supplier_view(request):
    return render(request, 'dashboard/supplier.html')

def customer_view(request):
    return render(request, 'dashboard/customer.html')