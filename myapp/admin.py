from django.contrib import admin

# myapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("Extra info", {"fields": ("phone", "user_status", "role")}),)
    list_display = ("username", "email", "phone", "birthdate", "role", 'created_at', "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "role", "user_status")
    search_fields = ("username", "email", "phone",)