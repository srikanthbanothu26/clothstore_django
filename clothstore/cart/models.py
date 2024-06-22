from django.db import models
from django.conf import settings
from store.models import Shirt


# Create your models here.
class Cart(models.Model):
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name="cart")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        default=None,
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.shirt.name}-{self.shirt.id}"

from django.conf import settings

class Address(models.Model):
    first_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        default=None,
    )

    def __str__(self) -> str:
        return f"{self.first_name}-{self.user.id}"
