from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shirt, WishList, ShirtImage, order_list
from cart.models import Address
from .forms import ShirtModelForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from cart.models import Cart


@login_required
def products(request):

    search_query = request.GET.get("search", "")

    user = request.user

    # get shirts from the database based on the search query
    if search_query:
        # http://localhost/store/shirts?search=green -> search_query = green
        # name or category
        shirts = Shirt.objects.filter(
            name__icontains=search_query
        ) | Shirt.objects.filter(category__icontains=search_query)
    else:
        shirts = Shirt.objects.all()

    for shirt in shirts:
        shirt.is_wished = False
        # check if the shirt is in the wishlist
        if shirt.wishlist.filter(user=user).exists():
            shirt.is_wished = True
            print("shirt.is_wished", shirt.is_wished)

    return render(request, "shirts_home.html", {"shirts": shirts})


def test_view(request):
    students = [
        {"name": "John", "last_name": "Doe", "age": 24, "email": "john@mail.com"},
        {"name": "Jane", "last_name": "Doe", "age": 22, "email": "jane@mail.com"},
    ]
    return render(request, "test.html", {"stus": students})


@csrf_protect
def new_product(request):
    if request.method == "POST":
        form = ShirtModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("/store/shirts")

    form = ShirtModelForm()
    return render(request, "new_product.html", {"form": form})


# http://localhost/store/whishlist?shirt_id=1
@login_required
def add_to_wishlist(request):
    shirt_id = request.GET.get("shirt_id")

    if not shirt_id:
        return JsonResponse({"error": "shirt_id is required"})

    # get the shirt object from the shirt id
    shirt = Shirt.objects.get(id=shirt_id)
    user = request.user
    # create a wishlist object
    whishObject = WishList(shirt=shirt, user=user)

    # save the wishlist object
    whishObject.save()

    return JsonResponse({"success": "Shirt added to wishlist"})


@login_required
def remove_from_wishlist(request, shirt_id):

    if not shirt_id:
        return JsonResponse({"error": "shirt_id is required"})

    # get the shirt object from the shirt id
    shirt = Shirt.objects.get(id=shirt_id)
    user = request.user
    # remove the shirt from the wishlist
    WishList.objects.filter(shirt=shirt, user=user).delete()

    return JsonResponse({"success": "Shirt removed from wishlist"})


@login_required
def product_view(request, product_id):
    shirt = Shirt.objects.get(id=product_id)
    user = request.user
    shirt.is_wished = shirt.wishlist.filter(user=user).exists()
    
    images=ShirtImage.objects.filter(shirt=shirt)
    
    return render(request, "product.html", {"shirt": shirt, "images": images})


from django.http import HttpResponse

def order_page(request, shirt_id):
    shirt = get_object_or_404(Shirt, pk=shirt_id)
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'order_page.html', {'shirt': shirt,'addresses': addresses})


def make_payment(request, shirt_id):
    if request.method == 'POST':
        return HttpResponse("Payment processed for shirt ID: {}".format(shirt_id))
    else:
        return redirect('order_page', shirt_id=shirt_id)
    
    
def add_new_address(request, shirt_id):
    if request.method=="POST":
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
        return redirect('order_page', shirt_id=shirt_id)
    
    return render(request,"address_form.html")

from django.contrib import messages
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    shirt_id = request.POST.get('shirt_id')  # Retrieve shirt_id from POST data
    address.delete()
    messages.success(request, 'Address has been deleted.')
    
    # Redirect to order_page with shirt_id
    return redirect('order_page', shirt_id=shirt_id)

def wishlist(request):
    user = request.user
    wishlist=WishList.objects.filter(user=user).select_related('shirt')
    return render(request, "wishlist.html", {"wishlist": wishlist})


@login_required
def Remove_from_Wishlist(request, shirt_id):
    if not shirt_id:
        return JsonResponse({"error": "shirt_id is required"})

    # get the shirt object from the shirt id
    shirt = get_object_or_404(Shirt, id=shirt_id)
    user = request.user
    # remove the shirt from the wishlist
    WishList.objects.filter(shirt=shirt, user=user).delete()

    return redirect('wlist')



@login_required
def make_order(request, shirt_id):
        shirt = get_object_or_404(Shirt, id=shirt_id)
        user = request.user
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, id=address_id, user=user)
        
        # Create and save the order
        order = order_list.objects.create(shirt=shirt, user=user, address=address)
        
        return redirect('order_details', order_id=order.id)
    

@login_required
def order_details(request, order_id):
    order = get_object_or_404(order_list, id=order_id, user=request.user)
    return render(request, 'order_details.html', {'order': order})