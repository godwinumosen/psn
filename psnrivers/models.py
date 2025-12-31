from django.db import models
from django.urls import reverse
from django.conf import settings

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
