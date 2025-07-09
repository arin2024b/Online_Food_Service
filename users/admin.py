from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = [AddressInline]
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    additional_fields = ('Additional Info', {'fields': ('phone', 'profile_picture')})
    if BaseUserAdmin.fieldsets:
        fieldsets = BaseUserAdmin.fieldsets + (additional_fields,)
    else:
        fieldsets = (additional_fields,)

admin.site.register(User, UserAdmin)
admin.site.register(Address)
