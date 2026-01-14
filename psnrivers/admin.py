from django.contrib import admin
# Register your models here.
from . import models
from .models import ClearanceApplication,Notification,UpcominEventsPsnRivers,NewsletterSubscriber
from .models import PsnRiversPost,AboutPsnRivers,NewsAndEventsPsnRivers,ContactMessage,PsnRiversExecutive

#The main post model admin
class PsnRiversPostModelAdmin (admin.ModelAdmin):
    prepopulated_fields = {'psnriver_slug': ('psnriver_title',)}
    list_display = ['psnriver_title','psnriver_description','psnriver_author']
admin.site.register(PsnRiversPost, PsnRiversPostModelAdmin)

#The about in home page post model admin
class AboutPsnRiversModelAdmin (admin.ModelAdmin):
    prepopulated_fields = {'about_psnriver_slug': ('about_psnriver_title',)}
    list_display = ['about_psnriver_title','about_psnriver_description','about_psnriver_author']
admin.site.register(AboutPsnRivers, AboutPsnRiversModelAdmin)

#The about in news and events page  admin
class NewsAndEventsPsnRiverslAdmin (admin.ModelAdmin):
    prepopulated_fields = {'newsandevents_psnriver_slug': ('newsandevents_psnriver_title',)}
    list_display = ['newsandevents_psnriver_title','newsandevents_psnriver_description','newsandevents_psnriver_author']
admin.site.register(NewsAndEventsPsnRivers, NewsAndEventsPsnRiverslAdmin)




class UpcominEventsPsnRiversAdmin (admin.ModelAdmin):
    prepopulated_fields = {'upcoming_newsandevents_psnriver_slug': ('upcoming_newsandevents_psnriver_title',)}
    list_display = ['upcoming_newsandevents_psnriver_title','upcoming_newsandevents_psnriver_author']
admin.site.register(UpcominEventsPsnRivers, UpcominEventsPsnRiversAdmin)



@admin.register(ClearanceApplication)
class ClearanceApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'membership_number',
        'full_name',
        'technical_group',
        'clearance_year',
        'status',  # ✅ property works here
        'submitted_at',
    )
    list_filter = ('technical_group', 'clearance_year')  # remove 'status' from filter
    search_fields = ('user__email', 'membership_number', 'full_name')
    ordering = ('-submitted_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'user__email')


    
class ContactMessageModelAdmin (admin.ModelAdmin):
    list_display = ['first_name','last_name','email','created_at']
admin.site.register(ContactMessage, ContactMessageModelAdmin)


class NewsletterSubscriberModelAdmin (admin.ModelAdmin):
    list_display = ['email','subscribed_at']
admin.site.register(NewsletterSubscriber, NewsletterSubscriberModelAdmin)


class PsnRiversExecutiveModelAdmin (admin.ModelAdmin):
    list_display = ['psnriver_executive_name','psnriver_executive_position']
admin.site.register(PsnRiversExecutive, PsnRiversExecutiveModelAdmin)



