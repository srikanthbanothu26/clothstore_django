# store/urls.py
from django.urls import path
from .views import ( products, add_to_wishlist,
                    remove_from_wishlist, product_view, order_page,make_payment, add_new_address, 
                    delete_address, wishlist, Remove_from_Wishlist, make_order, order_details
)

urlpatterns = [
    path("", products, name="store"),
    path("store/wlist",wishlist,name="wlist"),
    path("store/wishlist", add_to_wishlist, name="wishlist"),
    path("store/remove-wishlist/<int:shirt_id>", remove_from_wishlist, name="remove_wishlist"),
    path("store/product/<int:product_id>/", product_view, name="product_view"),
    path('store/order/<int:shirt_id>/', order_page, name='order_page'),
    path('store/make_payment/<int:shirt_id>/', make_payment, name='make_payment'),
    path('store/add_new_address/<int:shirt_id>/', add_new_address, name="add_new_address"),
    path('store/delete_address/<int:address_id>/', delete_address, name='delete_address'),
    path('wishlist/remove/<int:shirt_id>/', Remove_from_Wishlist, name='remove_from_wishlist'),
    path('make_order/<int:shirt_id>/', make_order, name='make_order'),
    path('order_details/<int:order_id>/', order_details, name='order_details'),
]
