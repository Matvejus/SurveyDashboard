from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from organization.models import OrgProfile

class CustomUserCreationForm(UserCreationForm):
    temp_license_code = forms.UUIDField()

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
            "temp_license_code",
        )

    def clean(self):
        cleaned_data = super().clean()
        organization = cleaned_data.get('organization')
        temp_license_code = cleaned_data.get('temp_license_code')
        
        if organization and temp_license_code:
            if not OrgProfile.objects.filter(title=organization.title, license_code=temp_license_code).exists():
                raise forms.ValidationError("Invalid license code for the selected organization. Please enter a correct license code.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.organization = OrgProfile.objects.get(title=self.cleaned_data.get('organization').title, 
                                                    license_code=self.cleaned_data.get('temp_license_code'))
        if commit:
            user.save()

        return user