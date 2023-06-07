from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from organization.models import OrgProfile
from .utils import setup_groups_permissions

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "username",
            "organization",
            "collaboration_network",
            "position",
            "avatar",
        )

    def clean(self):
        cleaned_data = super().clean()
        organization = cleaned_data.get('organization')
        
        if organization:
            if not OrgProfile.objects.filter(title=organization.title).exists():
                raise forms.ValidationError("Invalid organization selected.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.organization = OrgProfile.objects.get(title=self.cleaned_data.get('organization').title)
        if commit:
            user.save()
            setup_groups_permissions(user)
        return user