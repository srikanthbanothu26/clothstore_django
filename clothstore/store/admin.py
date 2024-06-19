from django.contrib import admin
from .models import Shirt, ShirtSize, WishList, ShirtImage


class ShirtSizeInline(admin.TabularInline):
    model = ShirtSize
    extra = 1  # how many rows to show

class ShirtImagesInline(admin.TabularInline):
    model = ShirtImage
    extra = 1  # how many rows to show
    # limit the number of rows to show
    max_num = 4

class ShirtAdmin(admin.ModelAdmin):
    inlines = [ShirtSizeInline, ShirtImagesInline]


class WishListAdmin(admin.ModelAdmin):
    list_display = ["shirt", "user"]


# Register your models here.
admin.site.register(Shirt, ShirtAdmin)
admin.site.register(ShirtSize)
admin.site.register(WishList, WishListAdmin)