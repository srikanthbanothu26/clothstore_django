from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart
from store.models import Shirt
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages

@login_required
def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user)

    total_quantity = sum(item.quantity for item in cart)
    total_price = sum(item.price for item in cart)

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
        cart.update_price()
        cart.save()
        return JsonResponse({"success": "Shirt added to cart"})

    shirt = Shirt.objects.get(id=shirt_id)
    cart = Cart(shirt=shirt, user=user, price=shirt.discountPrice)
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

from django.contrib.auth.decorators import login_required
from .models import Address
from django.http import JsonResponse

@login_required
def checkout_page(request):
    cart=Cart.objects.filter(user=request.user)
    total_discount_price = sum(item.price for item in cart)
    addresses = Address.objects.filter(user=request.user)
    
    return render(request, 'checkout.html',{'addresses': addresses, "cart": cart, 'total_discount_price': total_discount_price })  # Ensure you have this template in your templates directory

from django.shortcuts import render
from django.http import JsonResponse
import requests

@login_required
def Add_Address(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        village = request.POST.get('village', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        apikey = "pk.ed10c7b21526a2babc266be91ccebef9"
        url = f"https://api.locationiq.com/v1/autocomplete.php?key={apikey}&q={village}%20{city}%20{state}&limit=5&dedupe=1"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                resp = response.json()

                # Assuming the first result is relevant, extract address details
                if resp:
                    first_result = resp[0]
                    near_address = first_result.get('display_address', 'N/A')
                    pincode = first_result.get('address', {}).get('postcode', 'N/A')

                    # Create the address object if all required fields are present
                    if first_name and email and village and city and state and pincode and phone:
                        Address.objects.create(
                            user=request.user,
                            first_name=first_name,
                            address=f"{village}, {city}, {state}",
                            near_address=near_address,
                            city=city,
                            state=state,
                            pincode=pincode,
                            mobile=phone
                        )
                        return JsonResponse({'success': True, 'message': 'Address added successfully!','redirect_url': ''})
                    else:
                        return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'No matching address found.'}, status=404)
            else:
                return JsonResponse({'success': False, 'message': 'Failed to fetch address details from API.'}, status=500)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

@login_required

def Delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address has been deleted.')
    return redirect("checkout")


from store.models import Order
def make_orders(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        selected_sizes = request.POST.getlist('size')  # get the list of selected sizes
        shirt_ids = request.POST.getlist('shirt_id')  # get the list of shirt ids

        try:
            selected_address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, 'Selected address does not exist.')
            return redirect('make_order')

        try:
            orders = []
            for shirt_id, size in zip(shirt_ids, selected_sizes):
                shirt = get_object_or_404(Shirt, id=shirt_id)
                order = Order.objects.create(
                    shirt=shirt,
                    user=request.user,
                    address=selected_address,
                    size=size,
                    quantity=1,
                )
                orders.append(order)
            order_details = ', '.join([f"{order.shirt.name} (Size: {order.size})" for order in orders])
            success_message = f"Orders placed successfully! You ordered: {order_details}."
            messages.success(request, success_message)

            return JsonResponse({
                'success': True,
                'message': success_message,
                'orders': [{'shirt': order.shirt.name, 'size': order.size} for order in orders]
            })
        except Exception as e:
            messages.error(request, f'Failed to create orders: {str(e)}')
            return redirect('make_orders')