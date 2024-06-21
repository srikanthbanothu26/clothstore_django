from django.db import models
from django.conf import settings

# Create your models here.
# If we want to create a shirt table which contain shirts infomation in sql
# the query would be like this
"""
CREATE TABLE shirt(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price INT,
    description TEXT,
    image VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sizes VARCHAR(100),
    color VARCHAR(100)
);



Similarly, in Django, we can create a model for the shirt table like this:



"""


SIZE_CHOICES = (
    ("XS", "Extra Small"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("XXL", "Extra Extra Large"),
)


CATEGORY_CHOICES = (
    ("Oversized", "Oversized"),
    ("Regular", "Regular"),
    ("Slim Fit", "Slim Fit"),
    ("Classic", "Classic"),
    ("Dropcut", "Dropcut"),
)


class Shirt(models.Model):

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    previewImage = models.ImageField(upload_to="shirt_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    discountPrice = models.IntegerField(default=0)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default="Regular"
    )

    def __str__(self):
        return f"{self.id}-{self.name}"
    
    def get_available_quantity(self, size):
        try:
            shirt_size = self.shirt_sizes.get(size=size)
            return shirt_size.quantity
        except ShirtSize.DoesNotExist:
            return 0


class ShirtImage(models.Model):
    image = models.ImageField(upload_to="shirt_images/")
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.shirt.name}-{self.shirt.id}"


# shirt1 -> ShirtSize(shirt=shirt1, size="S", quantity=10) (available sizes-> S, M, L, XL)
# shirt1 -> ShirtSize(shirt=shirt1, size="M", quantity=10) (available sizes-> XS, S, M, L, XL, XXL)
# shirt1 -> ShirtSize(shirt=shirt1, size="L", quantity=10)



# shirt1 -> ShirtSize(shirt=shirt1, size="S", quantity=10) (available sizes-> S, M, L, XL)
# shirt1 -> ShirtSize(shirt=shirt1, size="M", quantity=10) (available sizes-> XS, S, M, L, XL, XXL)
# shirt1 -> ShirtSize(shirt=shirt1, size="L", quantity=10)


class ShirtSize(models.Model):
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    quantity = models.IntegerField(default=0)  # 10
    # here we are creating a foreign key to the shirt table
    # on_delete=models.CASCADE means if the shirt is deleted then the shirt size will also be deleted
    # related_name is used to access the shirt size from the shirt table
    shirt = models.ForeignKey(
        Shirt, on_delete=models.CASCADE, related_name="shirt_sizes"
    )

    def __str__(self):
        return f"{self.shirt.name}-{self.size}"

class WishList(models.Model):
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name="wishlist")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
        default=None,
    )

    def __str__(self):
        return f"{self.shirt.name} - {self.user.username}"

    
from cart.models import Address

class order_list(models.Model):
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, choices=SIZE_CHOICES, default='M')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    
    

