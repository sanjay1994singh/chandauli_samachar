from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Profile", {"fields": ("phone", "profile_image", "bio", "city", "is_reporter")}),)
    list_display = ("username", "email", "phone", "is_reporter", "is_staff")
