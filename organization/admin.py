from django.contrib import admin
from .models import OrgProfile,CollaborationNetwork

# Register your models here.

class OrgProfileAdmin(admin.ModelAdmin):
    list_display = ('title', 'org_type', 'num_employees', 'founded')
    list_filter = ('org_type',)
    search_fields = ('title', 'org_type')

class CollaborationNetworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage', 'orchestrator')
    list_filter = ('stage',)
    search_fields = ('title', 'stage')

admin.site.register(OrgProfile, OrgProfileAdmin)
admin.site.register(CollaborationNetwork, CollaborationNetworkAdmin)