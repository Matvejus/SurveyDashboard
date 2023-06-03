from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.utils.translation import gettext_lazy as _

#set up authorization - same user model but with different accesss
#user groups: User_admin - Lori: controllls orchestrators, User_orchestrator - controlls his networks, adds questions; user - takes surveys
class CustomUser(AbstractUser):

    class UserType(models.TextChoices):

        SUPERVISOR = "SUPER", _("CONESU supervisor")
        ORCHESTRATOR = "ORCHESTRATOR", _("Orchestrator")
        COLLABORATOR = "COLLAB", _("Network collaborator")

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='First name')
    last_name = models.CharField(max_length=150, verbose_name='Last name')
    organization = models.ForeignKey('organization.OrgProfile', null=True, on_delete=models.SET_NULL, related_name='users')
    collaboration_network = models.ForeignKey('organization.CollaborationNetwork', null=True, on_delete=models.SET_NULL)
    role = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.COLLABORATOR,
    )
    position = models.CharField(max_length=150, verbose_name='Position')
    avatar = models.ImageField(upload_to="avatars", blank = True, null = True)
    temp_license_code = models.UUIDField(blank=True, null=True)

    class Meta:
        order_with_respect_to = 'organization'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organization}"
