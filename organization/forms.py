from django import forms
from .models import OrgProfile, Contact, CollaborationNetwork

class NewOrgForm(forms.ModelForm):
    class Meta:
        model = OrgProfile
        fields = '__all__'

class NewCollaborationForm(forms.ModelForm):
    class Meta:
        model = CollaborationNetwork
        fields = '__all__'

class ContactForm(forms.ModelForm):
     class Meta: 
          model = Contact
          fields ='__all__'