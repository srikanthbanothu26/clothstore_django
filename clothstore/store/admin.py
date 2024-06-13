from django.contrib import admin
from .models import Shirt, ShirtSize, WishList


class ShirtSizeInline(admin.TabularInline):
    model = ShirtSize
    extra = 1  # how many rows to show


class ShirtAdmin(admin.ModelAdmin):
    inlines = [ShirtSizeInline]


class WishListAdmin(admin.ModelAdmin):
    list_display = ["shirt", "user"]


# Register your models here.
admin.site.register(Shirt, ShirtAdmin)
admin.site.register(ShirtSize)
admin.site.register(WishList, WishListAdmin)