import uuid
from django.contrib import admin
from .models import OrgProfile,CollaborationNetwork, License

# Register your models here.
@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('code', 'used_for_org', 'used_for_network', 'active')
    list_filter = ('active', 'used_for_org', 'used_for_network')
    search_fields = ('code',)
    actions = ['deactivate_licenses']

    def deactivate_licenses(self, request, queryset):
        queryset.update(active=False)
    deactivate_licenses.short_description = "Deactivate selected licenses"

    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = uuid.uuid4().hex
        super().save_model(request, obj, form, change)

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