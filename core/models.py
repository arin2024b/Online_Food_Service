from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default='Laziz Khana')
    logo = models.ImageField(upload_to='site_logo/', blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.site_name

class AnalyticsEvent(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=100)
    event_data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} at {self.timestamp}"
