from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Notification, ContactMessage

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'address')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active', 'profile_picture')
    search_fields = ('username', 'email', 'address')
    list_filter = ('is_staff', 'is_active', 'date_joined')

admin.site.register(Notification)
admin.site.register(ContactMessage)
