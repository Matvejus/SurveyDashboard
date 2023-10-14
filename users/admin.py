from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext as _

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ["email", "first_name", "last_name", "organization", "avatar_thumb"]
    list_filter = ("organization",)
    search_fields = ("email", "first_name", "last_name", "organization__title")
    ordering = ("organization", "last_name")
    readonly_fields = ('last_login', 'date_joined', 'avatar_thumb')

    autocomplete_fields = ['organization', 'collaboration_network']
    
    def avatar_thumb(self, obj):
        return format_html('<img src="{}" width="30" height="30" />', obj.avatar.url) if obj.avatar else _("No Avatar")
    avatar_thumb.short_description = _('Avatar')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'organization', 'collaboration_network', 'position', 'avatar', 'biography', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (_('User'), {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'organization', 'collaboration_network', 'position', 'avatar', 'avatar_thumb', 'biography'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    actions = ['deactivate_users']

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = _("Deactivate selected users")

admin.site.register(CustomUser, CustomUserAdmin)
