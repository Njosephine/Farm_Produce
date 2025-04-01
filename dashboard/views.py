from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from dashboard.forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile


def index_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid Credentials"
            return render(request, "accounts/auth.html", {"error": error_message})

    return render(request, "accounts/auth.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index") 


@login_required
def home_view(request):
    return render(request, "dashboard/home.html")

@login_required
def profile_view(request):
    profile, created =Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})


def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

def products_view(request):
    return render(request, 'dashboard/products.html')

def purchases_view(request):
    return render(request, 'dashboard/purchase.html')

def sales_view(request):
    return render(request, 'dashboard/sales.html')