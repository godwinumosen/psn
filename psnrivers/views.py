from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from .models import PsnRiversPost,AboutPsnRivers,NewsAndEventsPsnRivers
from django.contrib import messages
from .forms import ClearanceApplicationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin  



def index (request):
    return render (request, 'psnrivers/home.html')

class HomeView(ListView): 
    model = PsnRiversPost 
    template_name = 'psnrivers/home.html'
    
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['about_psnrivers'] = AboutPsnRivers.objects.all()  
        return context    
        

#The first ArticleDetailView page down
class ArticleDetailView(DetailView):
    model = PsnRiversPost
    template_name = 'psnrivers/article_detail.html'
    def ArticleDetailViewPsnRiversPost(request, pk): 
        object = get_object_or_404(PsnRiversPost, pk=pk)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        return render(request, 'article_detail.html', {'detail': object})


# This is for the news and events pae
class NewsAndEventsView(ListView): 
    model = NewsAndEventsPsnRivers 
    template_name = 'psnrivers/news_events.html'

def contact (request):
    return render (request, 'psnrivers/contact.html')

def about (request):
    return render (request, 'psnrivers/about.html')

def who_we_are (request):
    return render(request, "psnrivers/who_we_are.html")

def aims (request):
    return render(request, "psnrivers/aims.html")

def code (request):
    return render(request, "psnrivers/code.html")

def constitution (request):
    return render(request, "psnrivers/constitution.html")

def executive (request):
    return render(request, "psnrivers/executive.html")

def directory (request):
    return render(request, "psnrivers/directory.html")


def member_portal (request):
    return render(request, "psnrivers/member_portal.html")



def track_status (request):
    return render(request, "psnrivers/track_status.html")


def review_applications (request):
    return render(request, "psnrivers/review_applications.html")


@login_required
def apply_clearance(request):
    if request.method == 'POST':
        form = ClearanceApplicationForm(
            request.POST,
            request.FILES,
            user=request.user   # 👈 ADD
        )
        if form.is_valid():
            clearance = form.save(commit=False)
            clearance.user = request.user
            clearance.save()
            messages.success(request, "Your clearance application has been submitted successfully!")
            return redirect('home')
    else:
        form = ClearanceApplicationForm(user=request.user)  # 👈 ADD

    return render(request, 'psnrivers/apply_clearance.html', {'form': form})
