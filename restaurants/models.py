from django.db import models
from users.models import User

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    operating_hours = models.CharField(max_length=100)
    delivery_radius = models.PositiveIntegerField(blank=True, null=True)
    minimum_order = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cuisine_type = models.CharField(max_length=100)
    rating = models.FloatField(blank=True, null=True)
    is_approved = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurants')

    def __str__(self):
        return self.name

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class AddOn(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='addons')

    def __str__(self):
        return f"{self.name} ({self.price})"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    add_ons = models.ManyToManyField(AddOn, blank=True, related_name='menu_items')
    is_available = models.BooleanField()
    variant = models.CharField(max_length=50, blank=True)  # e.g., small/large

    def __str__(self):
        return self.name
