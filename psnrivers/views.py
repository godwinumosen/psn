from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
#from .models import ServicesPagePicture,RealEstatePicture,FacilityManagementPicture,ConstructionPicture
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin  


def index (request):
    return render (request, 'psnrivers/index.html')

'''class HomeView(ListView): 
    model = DeusMagnusMainPost 
    template_name = 'psnrivers/home.html'
   
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        
        context['bash_ps'] = BashPicture.objects.all()  
        return context    '''
        
    
def news_events (request):
    return render (request, 'psnrivers/news_events.html')
    