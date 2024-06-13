from django.http import JsonResponse
from django.shortcuts import render
from .models import Cart
from store.models import Shirt

from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def cart_view(request):
    user = request.user

    cart = Cart.objects.filter(user=user)

    quantity = 0
    for c in cart:
        quantity += c.quantity

    return render(request, "cart.html", {"cart": cart, "quantity": quantity})


@login_required
def add_to_cart(request, shirt_id):
    if not shirt_id:
        return JsonResponse({"error": "shirt_id is invalid"})

    user = request.user

    cart = Cart.objects.filter(shirt_id=shirt_id, user=user)

    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()
        return JsonResponse({"success": "Shirt added to cart"})

    shirt = Shirt.objects.get(id=shirt_id)
    cart = Cart(shirt=shirt, user=user)
    cart.save()

    return JsonResponse({"success": "Shirt added to cart"})


@login_required
def remove_from_cart(request, shirt_id):
    if not shirt_id:
        return JsonResponse({"error": "shirt_id is invalid"})

    user = request.user

    cart = Cart.objects.filter(shirt_id=shirt_id, user=user)

    if cart.exists():
        cart = cart.first()
        cart.quantity -= 1

        if cart.quantity <= 0:
            cart.delete()
        else:
            cart.save()

    return JsonResponse({"success": "Shirt removed from cart"})


@login_required
def checkout_page(request):
    return render(request, "checkout.html")


@login_required
def address_page(request):
    return render(request, "address_page.html")