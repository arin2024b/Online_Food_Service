from django.db import models
from users.models import User, Address
from restaurants.models import Restaurant, MenuItem, AddOn

ORDER_STATUS_CHOICES = [
    ('placed', 'Order Placed'),
    ('preparing', 'Preparing'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # percent or fixed
    is_percentage = models.BooleanField()
    expiry = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(blank=True, null=True)
    used_count = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='placed')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    add_ons = models.ManyToManyField(AddOn, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # snapshot at order time

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user}"

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    status = models.CharField(max_length=20, choices=[
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
    ], default='assigned')
    estimated_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Delivery for {self.order}"
