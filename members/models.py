from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

MEMBERSHIP_CHOICES = [
    ('regular', 'Regular'),
    ('premium', 'Premium'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('member', 'Member'),
]

class User(AbstractUser):
    # Additional fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    pcn_number = models.CharField(max_length=50, blank=True, null=True)
    year_qualified = models.IntegerField(blank=True, null=True)
    pcn_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    passport_photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    years_experience = models.IntegerField(blank=True, null=True)
    area_of_practice = models.CharField(max_length=255, blank=True, null=True)
    membership_category = models.CharField(max_length=50, choices=MEMBERSHIP_CHOICES, default='regular')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username
