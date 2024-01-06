from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from organization.models import OrgProfile, CollaborationNetwork
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
        collaborationnetwork = cleaned_data.get('collaboration_network')
        
        if organization and not OrgProfile.objects.filter(id=organization.id).exists():
            raise forms.ValidationError("Invalid organization selected.")
        
        if collaborationnetwork and not CollaborationNetwork.objects.filter(id=collaborationnetwork.id).exists():
            raise forms.ValidationError("Invalid Network selected.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            setup_groups_permissions(user)
        return user

class CustomUserChangeForm(UserChangeForm):
    verify_password = forms.CharField(
        label="Current password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        help_text="Please enter your current password."
    )
    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Enter a new password.",
        required=False  # Making it optional
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Confirm the new password.",
        required=False  # Making it optional
    )
    
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'organization', 
                  'collaboration_network', 'position', 'avatar', 'biography')
        exclude = ('password',)

    password = None
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")
        
        if password1 or password2:
            if password1 != password2:
                self.add_error('new_password2', "The two password fields didn’t match.")
        
        return cleaned_data
    
    def clean_verify_password(self):
        password = self.cleaned_data.get("verify_password")
        user = authenticate(username=self.instance.username, password=password)
        
        if user is None:
            raise forms.ValidationError("Incorrect password.")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")
        
        # If the user has entered a new password, update it.
        if new_password:
            user.set_password(new_password)
        
        if commit:
            user.save()
        return user