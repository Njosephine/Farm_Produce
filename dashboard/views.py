from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse # type: ignore

#Functions

def index(request):
    return render(request, 'dashboard/index.html')

def sidebar(request):
    return render(request, 'dashboard/sidebar.html')