from django import forms
from .models import TestSurvey, OrgProfile, Contact

class NewOrgForm(forms.ModelForm):
    class Meta:
        model = OrgProfile
        fields = '__all__'

class TestSurveyForm(forms.ModelForm):
       class Meta:
            model = TestSurvey
            fields = ['organization','satsified','period','occupation',]

class ContactForm(forms.ModelForm):
     class Meta: 
          model = Contact
          fields ='__all__'