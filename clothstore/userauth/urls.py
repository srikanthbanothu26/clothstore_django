from django.urls import path
from .views import register, login_view, logout_view

urlpatterns = [
    path("login/", login_view, name="customer_login"),
    path("register/", register, name="customer_register"),
    path("logout/", logout_view, name="customer_logout"),
]