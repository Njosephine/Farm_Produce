# from django.urls import path # type: ignore


from django.urls import path 
from dashboard.views import  index_view, logout_view,profile_view,dashboard_view, products_view, purchases_view, sales_view

urlpatterns = [
    # path("home/", home_view, name="home"),
    path("", index_view, name="index"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile" ),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('products/', products_view, name='products'),
    path('purchases/', purchases_view, name='purchases'),
    path('sales/', sales_view, name='sales'),
]


