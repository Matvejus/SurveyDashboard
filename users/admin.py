from django.contrib import admin
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "organization"]
    list_filter = ("organization",)
    search_fields = ("email", "first_name", "last_name", "organization__title")
    ordering = ("organization", "last_name")

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'organization', 'collaboration_network', 'position', 'avatar', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (_('User'), {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'organization', 'collaboration_network', 'position', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)