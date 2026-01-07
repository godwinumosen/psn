from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
#from .models import PsnRiversPost,
from django.contrib import messages
from .forms import ClearanceApplicationForm 
from django.utils import timezone
from .models import Notification,NewsAndEventsPsnRivers,AboutPsnRivers,UpcominEventsPsnRivers
from django.views.decorators.http import require_POST
from .models import ClearanceApplication
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin  



def index (request):
    return render (request, 'psnrivers/home.html')

class HomeView(TemplateView):
    template_name = 'psnrivers/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsandevents'] = NewsAndEventsPsnRivers.objects.all()
        context['about_psnrivers'] = AboutPsnRivers.objects.all()
        return context


# This is for the news and events pae
class NewsAndEventsView(ListView):
    model = NewsAndEventsPsnRivers
    template_name = 'psnrivers/news_events.html'
    context_object_name = 'articles'



#The first ArticleDetailView page for news and events
class ArticleDetailView(DetailView):
    model = NewsAndEventsPsnRivers
    template_name = 'psnrivers/news_article_detail.html'
    context_object_name = 'article'

    
class UpcomingNewsAndEventsView(ListView): 
    model = UpcominEventsPsnRivers 
    template_name = 'psnrivers/upcoming_news_events.html'

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
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(ClearanceApplication, id=app_id, user=request.user)

        if action == 'approve':
            application.status = 'approved'
            messages.success(request, f"{application.full_name}'s application has been approved.")
        elif action == 'decline':
            application.status = 'declined'
            decline_reason = request.POST.get('decline_reason', '')
            application.decline_reason = decline_reason
            messages.error(request, f"{application.full_name}'s application has been declined.")
        
        application.save()
        return redirect('track_status')  # reload page to show updated status

    # GET request
    applications = ClearanceApplication.objects.filter(user=request.user).order_by('-submitted_at')
    latest_application = applications.first()

    context = {
        'applications': applications,
        'latest_application': latest_application,
    }
    return render(request, 'psnrivers/track_status.html', context)





@login_required
def review_applications(request):
    # ✅ Handle approve/decline actions via POST
    if request.method == "POST":
        action = request.POST.get("action")
        app_id = request.POST.get("application_id")
        decline_reason = request.POST.get("decline_reason", "")

        if action and app_id:
            app = get_object_or_404(ClearanceApplication, id=app_id)
            
            if action == "approve":
                app.approved = True
                app.declined = False
                app.approved_at = timezone.now()
                app.decline_reason = ""
                messages.success(request, f"{app.full_name}'s application has been approved.")
            elif action == "decline":
                app.approved = False
                app.declined = True
                app.approved_at = None
                app.decline_reason = decline_reason
                messages.success(request, f"{app.full_name}'s application has been declined.")

            app.save()
            return redirect("review_applications")

    # ✅ Fetch applications for listing
    applications = ClearanceApplication.objects.all().order_by("-submitted_at")

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
def apply_clearance(request):
    if request.method == 'POST':
        form = ClearanceApplicationForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        if form.is_valid():
            clearance = form.save(commit=False)
            clearance.user = request.user
            clearance.save()

            # ✅ EMAIL SENT ONLY AFTER SUCCESSFUL SUBMISSION


            messages.success(
                request,
                "Your clearance application has been submitted successfully!"
            )
            return redirect('home')

    else:
        form = ClearanceApplicationForm(user=request.user)

    return render(
        request,
        'psnrivers/apply_clearance.html',
        {'form': form}
    )





@login_required
@require_POST
def approve_application(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)

    if request.user.is_staff:
        app.status = "Approved"
        app.approved_at = timezone.now()
        app.save()

        send_mail(
            "Clearance Approved",
            f"Congratulations {app.full_name},\n\n"
            f"Your clearance for {app.clearance_year} has been APPROVED.",
            None,
            [app.user.email],
        )

    return redirect('review_applications')



@login_required
@require_POST
def decline_application(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)

    if request.user.is_staff:
        app.status = "Declined"
        app.save()

        send_mail(
            "Clearance Declined",
            f"Dear {app.full_name},\n\n"
            "Unfortunately, your clearance application has been declined.\n"
            "Please contact support for more details.",
            None,
            [app.user.email],
        )

    return redirect('review_applications')







@login_required
def application_detail(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)

    # Handle approve/decline button clicks
    if request.method == 'POST' and not app.approved and not app.declined:
        action = request.POST.get('action')

        if action == 'approve':
            app.approved = True
            app.declined = False
            app.approved_at = timezone.now()
            app.save()

            messages.success(
                request,
                f"✅ Application for {app.full_name} has been approved successfully."
            )

        elif action == 'decline':
            decline_reason = request.POST.get('decline_reason')

            app.approved = False
            app.declined = True
            app.approved_at = None
            app.decline_reason = decline_reason
            app.save()

            messages.error(
                request,
                f"❌ Application for {app.full_name} has been declined. Reason: {decline_reason}"
            )

        return redirect('application_detail', app_id=app.id)

    return render(
        request,
        'psnrivers/application_detail.html',
        {'app': app}
    )



def profile(request):
    # Get the logged-in user
    user = request.user

    # Get latest clearance application
    latest_clearance = ClearanceApplication.objects.filter(
        user=user
    ).order_by('-submitted_at').first()

    # Get latest 5 notifications for the user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
    context = {
        "user": user,
        "clearance": latest_clearance,
        "notifications": notifications,
    }

    return render(request, "members/profile.html", context)
    
    

@login_required
def profile(request):
    latest_clearance = ClearanceApplication.objects.filter(
        user=request.user
    ).order_by('-submitted_at').first()

    notifications = Notification.objects.order_by('-created_at')[:10]

    return render(request, "members/profile.html", {
        "clearance": latest_clearance,
        "notifications": notifications
    })