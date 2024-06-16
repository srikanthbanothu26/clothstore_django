from django.http import JsonResponse
from django.shortcuts import render
from .models import Cart
from store.models import Shirt

from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user)

    total_quantity = sum(item.quantity for item in cart)
    total_price = sum((item.shirt.discountPrice or item.shirt.price) * item.quantity for item in cart)

    context = {
        'cart': cart,
        'quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, "cart.html", context)

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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Address
from django.http import JsonResponse

@login_required
def checkout_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')

        if not (first_name and email and address and city and state and zip_code and phone):
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        Address.objects.create(
            user=request.user,
            first_name=first_name,
            address=address,
            city=city,
            state=state,
            pincode=zip_code,
            mobile=phone
        )
        return JsonResponse({'success': True, 'message': 'Address added successfully!'})
    
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'checkout.html',{'addresses': addresses})  # Ensure you have this template in your templates directory

