from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import random

class Location(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    is_activation_used = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True, default='')
    phone = models.CharField(max_length=13, default='')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    profile_number = models.CharField(max_length=7, default='')
    old_email = models.CharField(max_length=255, blank=True, null=True, default='')
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def generate_profile_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(7)])

    def save(self, *args, **kwargs):
        if not self.profile_number:
            self.profile_number = self.generate_profile_number()
        super().save(*args, **kwargs)

class Scammer(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    brief_intro = models.CharField(max_length=255)
    modus_operandi = models.TextField(default='')
    phone = models.CharField(max_length=13, default='')
    is_verified = models.BooleanField(default=False)
    date_reported = models.DateField()
    last_date_reported = models.DateField(null=True, blank=True)
    votes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(CustomUser, related_name='voted_scammers', blank=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    scammer = models.ForeignKey(Scammer, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scammer.name}"

class Case(models.Model):
    scammer = models.ForeignKey(Scammer, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=13, default='')
    account_name = models.CharField(max_length=255, default='')
    bank_name = models.CharField(max_length=255, default='')
    case_details = models.TextField(default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_reported = models.DateField()
    is_verified = models.BooleanField(default=False)
    last_date_reported = models.DateField(null=True, blank=True)

    POLICE_REPORT_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]
    police_report = models.BooleanField(choices=POLICE_REPORT_CHOICES, default=False)

    def __str__(self):
        return self.case_details
