from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime, date

class PsnRiversPost(models.Model):
    psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    psnriver_description = models.TextField()
    psnriver_slug = models.SlugField (max_length=255,blank=True, null=True)
    psnriver_img = models.ImageField(upload_to='images/') 
    psnriver_publish_date = models.DateTimeField (auto_now_add= True)
    psnriver_author = models.ForeignKey(User, on_delete=models.CASCADE)

       
    class Meta:
        ordering =['-psnriver_publish_date']
    
    def __str__(self):
        return self.psnriver_title + ' | ' + str(self.psnriver_author)
    
    def get_absolute_url(self):
        return reverse('home')
    
    
#This one is the one on the home page     
class AboutPsnRivers(models.Model):
    about_psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    about_psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    about_psnriver_description = models.TextField()
    about_psnriver_description2 = models.TextField()
    about_psnriver_slug = models.SlugField (max_length=255,blank=True, null=True)
    about_psnriver_img = models.ImageField(upload_to='images/') 
    about_psnriver_publish_date = models.DateTimeField (auto_now_add= True)
    about_psnriver_author = models.ForeignKey(User, on_delete=models.CASCADE)

       
    class Meta:
        ordering =['-about_psnriver_publish_date']
    
    def __str__(self):
        return self.about_psnriver_title + ' | ' + str(self.about_psnriver_author)
    
    def get_absolute_url(self):
        return reverse('home')
    
    
class NewsAndEventsPsnRivers(models.Model):
    newsandevents_psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    newsandevents_psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    newsandevents_psnriver_description = models.TextField()
    newsandevents_psnriver_slug = models.SlugField (max_length=255,blank=True, null=True)
    newsandevents_psnriver_img = models.ImageField(upload_to='images/') 
    newsandevents_psnriver_publish_date = models.DateTimeField (auto_now_add= True)
    newsandevents_psnriver_author = models.ForeignKey(User, on_delete=models.CASCADE)

       
    class Meta:
        ordering =['-newsandevents_psnriver_publish_date']
    
    def __str__(self):
        return self. newsandevents_psnriver_title + ' | ' + str(self. newsandevents_psnriver_author)
    
    def get_absolute_url(self):
        return reverse('home')