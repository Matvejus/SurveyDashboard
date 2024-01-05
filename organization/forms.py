from django import forms
from django.core.exceptions import ValidationError
from .models import OrgProfile, Contact, CollaborationNetwork, License

class NewOrgForm(forms.ModelForm):
    license_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter License Code'}), label="License Code")

    class Meta:
        model = OrgProfile
        fields = ['title', 'org_type', 'vision', 'num_employees', 'founded', 'email', 'license_code']  # list all fields except the original 'license' field

    def clean_license_code(self):
        license_code = self.cleaned_data.get("license_code")
        try:
            license_obj = License.objects.get(code=license_code)
        except License.DoesNotExist:
            raise ValidationError("Invalid license code provided.")

        return license_code

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        org_profile = super().save(commit=False)
        license_code = self.cleaned_data.get("license_code")
        org_profile.license = License.objects.get(code=license_code)

        if commit:
            org_profile.save()
            self.save_m2m()

        return org_profile

class NewCollaborationForm(forms.ModelForm):
    license_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter License Code'}), label="License Code")

    class Meta:
        model = CollaborationNetwork
        fields = ['title', 'stage', 'orchestrator', 'collaborators',]

    def clean_license_code(self):
        license_code = self.cleaned_data.get("license_code")
        try:
            license_obj = License.objects.get(code=license_code)
        except License.DoesNotExist:
            raise ValidationError("Invalid license code provided.")

        return license_code
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        Collaborationnetwork = super().save(commit=False)
        license_code = self.cleaned_data.get("license_code")
        Collaborationnetwork.license = License.objects.get(code=license_code)

        if commit:
            Collaborationnetwork.save()
            self.save_m2m()

        return Collaborationnetwork



class ContactForm(forms.ModelForm):
     class Meta: 
          model = Contact
          fields ='__all__'