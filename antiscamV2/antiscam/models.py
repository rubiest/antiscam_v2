from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_activation_used = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True, default='')