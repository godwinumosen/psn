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
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import ClearanceApplication
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



@login_required
def track_status(request):
    applications = ClearanceApplication.objects.filter(user=request.user).order_by('-submitted_at')
    latest_application = applications.first()

    context = {
        'applications': applications,
        'latest_application': latest_application,
    }
    return render(request, 'psnrivers/track_status.html', context)



@login_required
def apply_clearance(request):
    if request.method == 'POST':
        form = ClearanceApplicationForm(request.POST, request.FILES, user=request.user)  # 👈 pass user here
        if form.is_valid():
            clearance = form.save(commit=False)
            clearance.user = request.user
            clearance.save()
            messages.success(request, "Your clearance application has been submitted successfully!")
            return redirect('home')  # or any page you want
    else:
        form = ClearanceApplicationForm(user=request.user)  # 👈 pass user here too

    return render(request, 'psnrivers/apply_clearance.html', {'form': form})





@login_required
def review_applications(request):
    # ✅ Handle approve/decline actions
    action = request.GET.get('action')
    app_id = request.GET.get('id')
    if action in ['approve', 'decline'] and app_id:
        app = get_object_or_404(ClearanceApplication, id=app_id)
        if action == 'approve':
            app.approved = True
            app.declined = False
            app.approved_at = timezone.now()
        elif action == 'decline':
            app.approved = False
            app.declined = True
            app.approved_at = None
        app.save()
        return redirect('review_applications')  # Reload page after action

    # ✅ Fetch applications for listing
    applications = ClearanceApplication.objects.all()

    # ✅ Stats cards
    total_applications = applications.count()
    pending_count = applications.filter(approved=False, declined=False).count()
    approved_count = applications.filter(approved=True).count()
    declined_count = applications.filter(declined=True).count()

    context = {
        'applications': applications,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'declined_count': declined_count,
    }
    return render(request, 'psnrivers/review_applications.html', context)


@login_required
@require_POST
def approve_application(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)
    if request.user.is_staff:
        app.approved = True
        app.approved_at = timezone.now()
        app.save()
    return redirect('review_applications')

@login_required
@require_POST
def decline_application(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)
    if request.user.is_staff:
        app.approved = False
        app.approved_at = timezone.now()
        app.save()
    return redirect('review_applications')


@login_required
def application_detail(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)
    return render(request, 'psnrivers/application_detail.html', {'app': app})