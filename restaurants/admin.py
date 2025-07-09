from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, AddOn

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine_type', 'rating', 'is_approved', 'minimum_order')
    list_filter = ('cuisine_type', 'is_approved')
    search_fields = ('name', 'address', 'cuisine_type')

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    list_filter = ('restaurant',)
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'variant')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'restaurant')
    list_filter = ('restaurant',)
    search_fields = ('name',)
