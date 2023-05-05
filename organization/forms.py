from django import forms
from .models import OrgProfile, Contact

class NewOrgForm(forms.ModelForm):
    class Meta:
        model = OrgProfile
        fields = '__all__'


class ContactForm(forms.ModelForm):
     class Meta: 
          model = Contact
          fields ='__all__'