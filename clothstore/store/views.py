from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Shirt, WishList
from .forms import ShirtModelForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


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

from django.shortcuts import render, get_object_or_404
@login_required
def product_view(request, product_id):
    shirt = get_object_or_404(Shirt, id=product_id)
    return render(request, "product.html", {"shirt": shirt})