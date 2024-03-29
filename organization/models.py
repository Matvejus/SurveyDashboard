from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
import uuid

from django.utils.translation import gettext_lazy as _

class License(models.Model):
    code = models.UUIDField(blank=True, null=True)
    used_for_org = models.BooleanField(default=False)
    used_for_network = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def is_fully_used(self):
        return self.used_for_org and self.used_for_network

    def deactivate(self):
        self.active = False
        self.save()

    def __str__(self):
        return str(self.code)

#Model for organization (stakeholder)
class OrgProfile(models.Model):
        #choice class
        class OrganizationType(models.TextChoices):
             
             GOVERMENT_FEDERAL = "GVR_F", _("Government - Federal or state government")
             GOVERMENT_LOCAL = "GVR_L", _("Government - Local agency")
             NGO = "NGO", _("NGO - National or International")
             PRIVATE_MULTI = "PRIV_MULTI", _("Private sector - Multinational Corporation")
             PRIVATE_NATIONAL = "PRIV_NATIONAL", _("Private sector - National Corporation")
             SMALLHOLDER = "SMALLHOLDER", _("Smallholder producer")
             PRODUCER = "PRODUCER", _("Producer organization")
             FARMERS = "FARMERS_ASC", _("Farmers' association")
             LABOR_UNION = "LABOR_UNION", _("Labor union")
             OTHER = "OTHER", _("Other civil society organization")

        title = models.CharField(max_length=200, blank=False)
        org_type = models.CharField(max_length = 250, choices=OrganizationType.choices)
        vision = models.CharField(max_length=250, blank=True)
        num_employees = models.CharField(max_length=20)
        founded = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(datetime.datetime.now().year)])
        email = models.EmailField(max_length=255, blank=False)
        license = models.ForeignKey(License, on_delete=models.CASCADE)

        def __str__(self):
            return f"{self.title}"
        
        
#model to gather users in one network
class CollaborationNetwork(models.Model):
    #Stage choices of the collaboration| start, middle, end - changes surveys avalibale for participants
    class NetworkStage(models.TextChoices):
         
         START = "START", _("Starting phase of the collaboration")
         MIDDLE = "MIDDLE", _("Middle stage")
         END = "END", _("Final stage of the collaboration")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=160)
    stage = models.CharField(max_length = 20, choices=NetworkStage.choices)
    orchestrator = models.ForeignKey('users.CustomUser', on_delete=models.DO_NOTHING, related_name='orchestrator',)
    collaborators = models.ManyToManyField('users.CustomUser', related_name='collaborators',)
    license = models.ForeignKey(License, on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.title} - Orchestrator: {self.orchestrator}"

    
#Model for contact form on landing page. Might create an abstract user model to store often used fields
class Contact(models.Model):
    name = models.CharField(max_length=100, name="Full name")
    organization = models.CharField(max_length=100, name = "Company")
    role = models.CharField(max_length=100, name ="Role")
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20, blank = True)

    def __str__(self):
        return f"{self.name} {self.organization}-{self.role}"
