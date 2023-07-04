from django.contrib import admin
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "organization"]
    list_filter = ("organization",)
    search_fields = ("email", "first_name", "last_name", "organization__title")
    ordering = ("organization", "last_name")

admin.site.register(CustomUser, CustomUserAdmin)