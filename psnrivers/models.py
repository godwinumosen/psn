from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone  # ✅ important

class PsnRiversPost(models.Model):
    psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    psnriver_description = models.TextField()
    psnriver_slug = models.SlugField(max_length=255, blank=True, null=True)
    psnriver_img = models.ImageField(upload_to='images/')
    psnriver_publish_date = models.DateTimeField(auto_now_add=True)
    psnriver_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-psnriver_publish_date']

    def __str__(self):
        return f"{self.psnriver_title} | {self.psnriver_author}"

    def get_absolute_url(self):
        return reverse('home')


class AboutPsnRivers(models.Model):
    about_psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    about_psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    about_psnriver_description = models.TextField()
    about_psnriver_description2 = models.TextField()
    about_psnriver_slug = models.SlugField(max_length=255, blank=True, null=True)
    about_psnriver_img = models.ImageField(upload_to='images/')
    about_psnriver_publish_date = models.DateTimeField(auto_now_add=True)
    about_psnriver_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-about_psnriver_publish_date']

    def __str__(self):
        return f"{self.about_psnriver_title} | {self.about_psnriver_author}"

    def get_absolute_url(self):
        return reverse('home')


class NewsAndEventsPsnRivers(models.Model):
    newsandevents_psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    newsandevents_psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    newsandevents_psnriver_description = models.TextField()
    newsandevents_psnriver_slug = models.SlugField(max_length=255, blank=True, null=True)
    newsandevents_psnriver_img = models.ImageField(upload_to='images/')
    newsandevents_psnriver_publish_date = models.DateTimeField(auto_now_add=True)
    newsandevents_psnriver_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-newsandevents_psnriver_publish_date']

    def __str__(self):
        return f"{self.newsandevents_psnriver_title} | {self.newsandevents_psnriver_author}"

    def get_absolute_url(self):
        return reverse('home')





CLEARANCE_YEAR_CHOICES = [
    ('2024', '2024'),
    ('2025', '2025'),
    ('2026', '2026'),
]

TECHNICAL_GROUP_CHOICES = [
    ('Community Pharmacy', 'Community Pharmacy'),
    ('Hospital Pharmacy', 'Hospital Pharmacy'),
    ('Industrial Pharmacy', 'Industrial Pharmacy'),
    ('Administrative Pharmacy', 'Administrative Pharmacy'),
    ('Academic Pharmacy', 'Academic Pharmacy'),
    ('Regulatory Pharmacy', 'Regulatory Pharmacy'),
]

class ClearanceApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    technical_group = models.CharField(max_length=50, choices=TECHNICAL_GROUP_CHOICES)
    clearance_year = models.CharField(max_length=4, choices=CLEARANCE_YEAR_CHOICES)
    proof_of_payment = models.FileField(upload_to='clearance/payments/')
    supporting_document = models.FileField(upload_to='clearance/supporting/', blank=True, null=True)
    declaration_confirmed = models.BooleanField(default=False)  
    submitted_at = models.DateTimeField(auto_now_add=True)

    # ✅ Status fields
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.email} | {self.clearance_year} | {self.technical_group}"

    # ✅ Computed status property
    @property
    def status(self):
        if self.approved:
            return "Approved"
        elif self.declined:
            return "Declined"
        else:
            return "Pending"