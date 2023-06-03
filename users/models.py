from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='First name')
    last_name = models.CharField(max_length=150, verbose_name='Last name')
    organization = models.ForeignKey('organization.OrgProfile', null=True, on_delete=models.SET_NULL, related_name='users')
    collaboration_network = models.ForeignKey('organization.CollaborationNetwork', null=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=150, verbose_name='Position')
    avatar = models.ImageField(upload_to="avatars", blank = True, null = True)

    class Meta:
        order_with_respect_to = 'organization'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organization}"
