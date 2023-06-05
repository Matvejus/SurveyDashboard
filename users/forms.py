from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from organization.models import OrgProfile

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

        collaborator_group, created = Group.objects.get_or_create(name='COLLABORATOR')
        user.groups.add(collaborator_group)
        
        #collaborator permissions
        permission_codes = [
            'view_answer',
            'view_question',
            'view_survey',
            'add_useranswer',
            'view_useranswer',
            'view_collaborationnetwork',
            'view_orgprofile',
            'add_testsurvey',
            'view_testsurvey',
            'change_customuser',
            'delete_customuser',
            'view_customuser',
        ]

        # permissions assign to
        permissions = Permission.objects.filter(codename__in=permission_codes)
        collaborator_group.permissions.set(permissions)
        return user