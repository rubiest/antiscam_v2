from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    is_activation_used = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True, default='')
    phone = models.CharField(max_length=13, default='')
    location = models.CharField(max_length=30, default='')
    profile_number = models.CharField(max_length=7, default='')
    old_email = models.CharField(max_length=255, blank=True, null=True, default='')

    def generate_profile_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(7)])

    def save(self, *args, **kwargs):
        if not self.profile_number:
            self.profile_number = self.generate_profile_number()
        super().save(*args, **kwargs)