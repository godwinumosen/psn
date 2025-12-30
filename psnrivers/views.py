from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from .models import PsnRiversPost
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin  


def index (request):
    return render (request, 'psnrivers/home.html')

class HomeView(ListView): 
    model = PsnRiversPost 
    template_name = 'psnrivers/home.html'
    
    #def get_context_data(self, **kwargs):  
     #   context = super().get_context_data(**kwargs)
        
        #context['bash_ps'] = BashPicture.objects.all()  
        #return context    
        

#The first ArticleDetailView page down
class ArticleDetailView(DetailView):
    model = PsnRiversPost
    template_name = 'psnrivers/article_detail.html'
    def ArticleDetailViewPsnRiversPost(request, pk): 
        object = get_object_or_404(PsnRiversPost, pk=pk)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        return render(request, 'article_detail.html', {'detail': object})

        
        
        
def news_events (request):
    return render (request, 'psnrivers/news_events.html')

def contact (request):
    return render (request, 'psnrivers/contact.html')
    