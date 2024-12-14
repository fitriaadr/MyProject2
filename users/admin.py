# users/admin.py
from django.contrib import admin
from .models import Notification, ContactMessage

admin.site.register(Notification)
admin.site.register(ContactMessage)
