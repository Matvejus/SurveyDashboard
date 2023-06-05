from django.contrib import admin
from .models import OrgProfile,CollaborationNetwork, TestSurvey

# Register your models here.

admin.site.register(OrgProfile)
admin.site.register(CollaborationNetwork)
admin.site.register(TestSurvey)