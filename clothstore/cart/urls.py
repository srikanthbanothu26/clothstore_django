from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, checkout_page, Delete_address, Add_Address

urlpatterns = [
    path("", cart_view, name="cart"),
    path("add/<int:shirt_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:shirt_id>/", remove_from_cart, name="remove_from_cart"),
    path("checkout/", checkout_page, name="checkout"),
    path("Delete-Address/<int:address_id>/", Delete_address, name="Delete-Address"),
    path('Add-Address', Add_Address, name='Add_Address' )
]