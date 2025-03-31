# from django.urls import path # type: ignore

# from django.contrib.auth.views 
# from dashboard import views

# urlpatterns = [
#     path("auto/", views.sidebar, name ="sidebar"),

#     path("accounts/login/", login_view, name="login"),
#     path("accounts/logout/", LogoutView.as_view(), name="logout")
# ]
from django.urls import path 
from django.contrib.auth import views as auth_views
from dashboard.views import home_view, login_view, logout_view

urlpatterns = [
    path("home/", home_view, name="home"),
    path("auth/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]


