from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        PROCESSING = 'R', 'Processing'
        SHIPPED = 'S', 'Shipped'
        DELIVERED = 'D', 'Delivered'
        CANCELED = 'C', 'Cancelled'

    order_id = models.BigIntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(9223372036854775807)],
    )
    status = models.CharField(
        max_length=1, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    currency = models.CharField(max_length=5)
    shipping_cost = models.PositiveIntegerField()
    inclubing_taxes = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'  # pyright: ignore


class User(models.Model):
    order = models.OneToOneField(
        Order, related_name='user_details', on_delete=models.CASCADE
    )
    user_id = models.BigIntegerField(
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(9223372036854775807)],
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=(
                    r'^\+?(\d{1,4})?[\s\-\.]?\(?\d+\)'
                    r'?[\s\-\.]?\d+[\s\-\.]?\d+[\s\-\.]?\d+$'
                ),
                message=(
                    "Phone number must be entered in the format: "
                    "'+999(999)-999-9999'. Up to 18 digits allowed"
                ),
            )
        ],
    )


class Delivery(models.Model):
    class DeliveredType(models.TextChoices):
        PICKUP = 'P', 'Pickup'
        COURIER = 'C', 'Courier'

    order = models.OneToOneField(
        Order, related_name='delivery_details', on_delete=models.CASCADE
    )
    tracking_id = models.CharField(max_length=50, blank=True)
    tracking_url = models.URLField(max_length=500, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivery_type = models.CharField(
        max_length=1, choices=DeliveredType.choices, default=DeliveredType.COURIER
    )
    comment_to_delivery = models.TextField(max_length=5000, blank=True)
    address_1 = models.CharField(max_length=300)
    address_2 = models.CharField(max_length=300)
    postal_code = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=250)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.BigIntegerField(
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(9223372036854775807)],
    )
    name = models.CharField(max_length=300)
    image_url = models.URLField(max_length=1000)
    size = models.CharField(max_length=30)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(50)]
    )

    def __str__(self):
        return str(self.id)  # pyright: ignore

    def get_cost(self):
        return self.price * self.quantity
