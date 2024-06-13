from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, checkout_page, address_page

urlpatterns = [
    path("", cart_view, name="cart"),
    path("add/<int:shirt_id>", add_to_cart, name="add_to_cart"),
    path("remove/<int:shirt_id>", remove_from_cart, name="remove_from_cart"),
    path("checkout/", checkout_page, name="checkout"),
    path("new-address", address_page, name="new-address"),
]