from django.contrib import admin
# Register your models here.
from . import models
from .models import PsnRiversPost

#The DeusMagnus main post model admin
class PsnRiversPostModelAdmin (admin.ModelAdmin):
    prepopulated_fields = {'psnriver_slug': ('psnriver_title',)}
    list_display = ['psnriver_title','psnriver_description','psnriver_author']
admin.site.register(PsnRiversPost, PsnRiversPostModelAdmin)