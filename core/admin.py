from django.contrib import admin
from .models import SiteSetting, AnalyticsEvent

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone')

@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'timestamp')
    list_filter = ('event_type',)
