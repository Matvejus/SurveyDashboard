from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import CustomUser
import datetime
import uuid

from django.utils.translation import gettext_lazy as _




#Model for organization (stakeholder)
class OrgProfile(models.Model):
        #choice class
        class OrganizationType(models.TextChoices):
             
             GOVERMENT_FEDERAL = "GVR_F", _("Government - Federal or state government jurisdiction/agency")
             GOVERMENT_LOCAL = "GVR_L", _("Government - Local agency (e.g. district, municipality, regional)")
             NGO = "NGO", _("NGO - National or International")
             PRIVATE_MULTI = "PRIV_MULTI", _("Private sector - Multinational Corporation")
             PRIVATE_NATIONAL = "PRIV_NATIONAL", _("Private sector - National Corporation")
             SMALLHOLDER = "SMALLHOLDER", _("Smallholder producer")
             PRODUCER = "PRODUCER", _("Producer organization")
             FARMERS = "FARMERS_ASC", _("Farmers' association")
             LABOR_UNION = "LABOR_UNION", _("LABOR_UNION")
             OTHER = "OTHER", _("Other civil society organization (e.g. Women Association, Youth Association)")
             

        title = models.CharField(max_length=200, blank=False)
        org_type = models.CharField(choices=OrganizationType.choices)
        vision = models.CharField(max_length=250, blank=True)
        num_employees = models.CharField(max_length=20)
        founded = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(datetime.datetime.now().year)])
        email = models.EmailField(max_length=255, blank=False)
    

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
    stage = models.CharField(choices=NetworkStage.choices)
    orchestrator = models.ForeignKey(CustomUser)#Collaboration can be managed only by one person
    paticipants = models.ForeignKey(CustomUser)#Collaboration can have many participants

    def __str__(self):
            return f"{self.title} - Orchestrator: {self.orchestrator}"


#Basic survey model. It now stores both questions and answers, this is a simple solution that needs to be rebuild.
class TestSurvey(models.Model):
    STUDENT = 'STUD'
    EMPLOYEE = 'EMP'
    POSITION_CHOICE = [
            (STUDENT, 'Student'),
            (EMPLOYEE, 'Employee'),]
    
    organization = models.ForeignKey(OrgProfile, on_delete= models.CASCADE)
    satsified = models.IntegerField( validators=[MinValueValidator(1), MaxValueValidator(10)])
    period = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(40)])
    occupation = models.CharField(max_length=10, choices=POSITION_CHOICE)
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Surveys'

    
#Model for contact form on landing page. Might create an abstract user model to store often used fields
class Contact(models.Model):
    name = models.CharField(max_length=100, name="Full name")
    organization = models.CharField(max_length=100, name = "Company")
    role = models.CharField(max_length=100, name ="Role")
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20, blank = True)

    def __str__(self):
        return f"{self.name} {self.organization}-{self.role}"


