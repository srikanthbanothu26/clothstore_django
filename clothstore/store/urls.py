# store/urls.py
from django.urls import path
from .views import ( products, add_to_wishlist,
                     product_view, order_page,make_payment, add_new_address, 
                    delete_address, wishlist, Remove_from_Wishlist, make_order, order_details, all_orders,
                    order_successfull, delete_order, check_stock
)

urlpatterns = [
    path("", products, name="store"),
    path("store/wlist/",wishlist,name="wlist"),
    path("store/add-wishlist/<int:shirt_id>/", add_to_wishlist, name="wishlist"),
    path('store/remove-wishlist/<int:shirt_id>/', Remove_from_Wishlist, name='remove_from_wishlist'),
    path("store/product/<int:product_id>/", product_view, name="product_view"),
    path('store/order/<int:shirt_id>/', order_page, name='order_page'),
    path('store/make_payment/<int:shirt_id>/', make_payment, name='make_payment'),
    path('store/add_new_address/<int:shirt_id>/', add_new_address, name="add_new_address"),
    path('store/delete_address/<int:address_id>/', delete_address, name='delete_address'),
    
    path('make_order/<int:shirt_id>/', make_order, name='make_order'),
    path('order_details/<int:order_id>/', order_details, name='order_details'),
    path('all_orders',all_orders, name="all_orders"),
    path('order_successull/<int:order_id>/',order_successfull, name="order_successfull"),
    path('delete_order/<int:order_id>/', delete_order, name="delete_order"),
    path('check_stock/<int:shirt_id>/', check_stock, name="check_stock"),
    
]
