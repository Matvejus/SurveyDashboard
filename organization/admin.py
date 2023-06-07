from django.contrib import admin
from .models import OrgProfile, TestSurvey, CollaborationNetwork

# Register your models here.

admin.site.register(OrgProfile)
admin.site.register(TestSurvey)
admin.site.register(CollaborationNetwork)