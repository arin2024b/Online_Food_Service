from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255, default='')
    postal_code = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='Dhaka')
    is_default = models.BooleanField()

    def __str__(self):
        return f"{self.address}, {self.city} ({self.postal_code})"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # delivery addresses handled by Address model

    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return self.username
