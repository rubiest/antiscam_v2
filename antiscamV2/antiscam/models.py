from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
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

class Scammer(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    brief_intro = models.CharField(max_length=255)
    modus_operandi = models.TextField(default='')
    is_verified = models.BooleanField(default=False)
    date_reported = models.DateField(default='')
    last_date_reported = models.DateField(default='', null=True, blank=True)

    def __str__(self):
        return self.name