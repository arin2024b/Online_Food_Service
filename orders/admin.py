from django.contrib import admin
from .models import Order, OrderItem, PromoCode, Review, Delivery

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'total', 'status', 'timestamp')
    list_filter = ('status', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price')
    list_filter = ('menu_item',)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_percentage', 'expiry', 'usage_limit', 'used_count')
    list_filter = ('is_percentage',)
    search_fields = ('code',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'menu_item', 'rating', 'timestamp')
    list_filter = ('restaurant', 'menu_item', 'rating')
    search_fields = ('user__username', 'restaurant__name', 'menu_item__name')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_partner', 'status', 'estimated_time')
    list_filter = ('status',)
