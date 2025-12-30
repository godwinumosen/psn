from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime, date

class PsnRiversPost(models.Model):
    psnriver_title = models.CharField(max_length=255, blank=True, null=True)
    psnriver_status = models.CharField(max_length=255, blank=True, null=True)
    psnriver_description = models.TextField()
    psnriver_slug = models.SlugField (max_length=255,blank=True, null=True)
    deus_manus_img = models.ImageField(upload_to='images/') 
    psnriver_publish_date = models.DateTimeField (auto_now_add= True)
    psnriver_author = models.ForeignKey(User, on_delete=models.CASCADE)

       
    class Meta:
        ordering =['-psnriver_publish_date']
    
    def __str__(self):
        return self.psnriver_title + ' | ' + str(self.psnriver_author)
    
    def get_absolute_url(self):
        return reverse('home')