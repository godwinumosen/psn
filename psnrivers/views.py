from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth import get_user_model

from PIL import Image, ImageDraw
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from members.utils import send_clearance_email
from .forms import ClearanceApplicationForm
from .models import (
    Notification,
    NewsAndEventsPsnRivers,
    AboutPsnRivers,
    UpcominEventsPsnRivers,
    ClearanceApplication,
    ContactMessage,
    NewsletterSubscriber,
    PsnRiversExecutive,
)

User = get_user_model()



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


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("home")
    return render(request, "psnrivers/contact.html")


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
                app.save()

                # ✅ Email to user
                send_clearance_email(
                    user=app.user,
                    subject="Clearance Application Approved",
                    message=f"Hello {app.full_name},\n\n"
                            "Congratulations! Your"
                            f"{app.clearance_year} Clearance Application has been approved.\n\n"
                            "Thank you for completing the process.\n\n"
                            "You can now download your Proof of Clearance from your Member Dashboard.\n\n"
                            "How to access it:\n"
                            "1. Sign in via the Member Portal.\n"
                            "2. Click View Dashboard.\n"
                            "3. Click Download Clearance Certificate.\n\n"
                            "If you need any assistance, please contact the PSN Rivers Secretaria.\n\n"
                            "Warm regards,\n"
                            "Pharmaceutical Society of Nigeria\n"
                            "Rivers State Branch."
                )

                messages.success(request, f"{app.full_name}'s application has been approved successfully.")

            elif action == "decline":
                app.approved = False
                app.declined = True
                app.approved_at = None
                app.decline_reason = decline_reason
                app.save()

                # ✅ Email to user
                send_clearance_email(
                    user=app.user,
                    subject="Clearance Application Declined",
                    message=f"Hello {app.full_name},\n\n"
                            "Unfortunately, your clearance application for "
                            f"{app.clearance_year} has been declined.\n"
                            f"Reason: {decline_reason}\n\n"
                            "Please contact support if you need more information."
                )

                messages.success(request, f"{app.full_name}'s application has been declined.")

            return redirect("review_applications")

    # Fetch applications for listing
    applications = ClearanceApplication.objects.all().order_by("-submitted_at")

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

            # ✅ Email to user
            send_clearance_email(
                user=request.user,
                subject="Clearance Application Submitted",
                message=f"Hello {request.user.first_name or request.user.email},\n\n"
                        "Your clearance application has been submitted successfully.\n"
                        f"Clearance Year: {clearance.clearance_year}\n"
                        f"Technical Group: {clearance.technical_group}\n\n"
                        "We will notify you once it is reviewed."
            )

            # ✅ Optional: notify admins
            admin_emails = User.objects.filter(is_staff=True)
            for admin in admin_emails:
                send_clearance_email(
                    user=admin,
                    subject="New Clearance Application Submitted",
                    message=f"User {request.user.get_full_name()} submitted a clearance application "
                            f"for {clearance.clearance_year}."
                )

            messages.success(
                request,
                "Your clearance application has been submitted successfully!"
            )
            return redirect('member_portal')
    else:
        form = ClearanceApplicationForm(user=request.user)

    return render(request, 'psnrivers/apply_clearance.html', {'form': form})


@login_required
@require_POST
def approve_application(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)

    if request.user.is_staff:
        app.approved = True
        app.declined = False
        app.approved_at = timezone.now()
        app.decline_reason = ""
        app.save()

        # ✅ Email to user
        send_clearance_email(
            user=app.user,
            subject="Clearance Application Approved",
            message=f"Hello {app.full_name},\n\n"
                    "Congratulations! Your clearance application for "
                    f"{app.clearance_year} has been approved.\n\n"
                    "Thank you for completing the process."
        )

    return redirect('review_applications')



@login_required
@require_POST
def decline_application(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)

    if request.user.is_staff:
        app.approved = False
        app.declined = True
        app.approved_at = None
        app.save()

        # ✅ Email to user
        send_clearance_email(
            user=app.user,
            subject="Clearance Application Declined",
            message=f"Hello {app.full_name},\n\n"
                    "Unfortunately, your clearance application for "
                    f"{app.clearance_year} has been declined.\n\n"
                    "Please contact support if you need more information ."
        )

    return redirect('review_applications')



@login_required
def application_detail(request, app_id):
    app = get_object_or_404(ClearanceApplication, id=app_id)

    if request.method == 'POST' and not app.approved and not app.declined:
        action = request.POST.get('action')
        decline_reason = request.POST.get('decline_reason', '')

        if action == 'approve':
            app.approved = True
            app.declined = False
            app.approved_at = timezone.now()
            app.save()

            # ✅ Email to user
            send_clearance_email(
                user=app.user,
                subject="Clearance Application Approved",
                message=f"Hello {app.full_name},\n\n"
                        "Congratulations! Your clearance application for "
                        f"{app.clearance_year} has been approved.\n\n"
                        "Thank you for completing the process."
            )

            messages.success(
                request,
                f"✅ Application for {app.full_name} has been approved successfully."
            )

        elif action == 'decline':
            app.approved = False
            app.declined = True
            app.approved_at = None
            app.decline_reason = decline_reason
            app.save()

            # ✅ Email to user
            send_clearance_email(
                user=app.user,
                subject="Clearance Application Declined",
                message=f"Hello {app.full_name},\n\n"
                        "Unfortunately, your clearance application for "
                        f"{app.clearance_year} has been declined.\n"
                        f"Reason: {decline_reason}\n\n"
                        "Please contact support if you need more information."
            )

            messages.error(
                request,
                f"❌ Application for {app.full_name} has been declined. Reason: {decline_reason}"
            )

        return redirect('application_detail', app_id=app.id)

    return render(request, 'psnrivers/application_detail.html', {'app': app})



    
@login_required
def profile(request):
    # Get the latest clearance application for the logged-in user
    latest_clearance = ClearanceApplication.objects.filter(
        user=request.user
    ).order_by('-submitted_at').first()

    # Get latest 10 notifications
    notifications = Notification.objects.order_by('-created_at')[:10]

    context = {
        "user": request.user,
        "clearance": latest_clearance,   # ✅ pass this to template
        "notifications": notifications,
    }

    return render(request, "members/profile.html", context)

    
    

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, "Thank you for subscribing!")
        else:
            messages.error(request, "Please enter a valid email.")

    return redirect(request.META.get("HTTP_REFERER", "/"))



class ExecutivesView(ListView):
    model = PsnRiversExecutive
    template_name = 'psnrivers/executive.html'
    context_object_name = 'object_list'
    
    

@login_required
def profile_pdf(request):
    clearance = ClearanceApplication.objects.filter(
        user=request.user
    ).order_by('-submitted_at').first()

    if not clearance or not clearance.approved:
        return HttpResponseForbidden(
            "You cannot download this PDF until your clearance is approved."
        )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="profile_{request.user.username}.pdf"'

    # ===== PDF Setup =====
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    left_margin = 50
    right_margin = 50
    current_y = height - 60

    # ===== HEADER =====
    p.setFont("Helvetica-Bold", 30)
    p.setFillColor(colors.HexColor("#2d6a4f"))
    p.drawCentredString(width / 2, current_y, "PSN Rivers Clearance Approval")
    current_y -= 60

    # ===== PROFILE IMAGE =====
    img_size = 120  # bigger image
    if request.user.passport_photo:
        try:
            img = ImageReader(request.user.passport_photo.path)
            p.drawImage(
                img,
                (width - img_size) / 2,   # centered
                current_y - img_size,
                img_size,
                img_size,
                mask='auto'
            )
        except Exception:
            pass
    current_y -= img_size + 30  # spacing after image

    # ===== PROFILE CARD =====
    profile_data = [
        ("Full Name", request.user.get_full_name()),
        ("PCN Registration Number", getattr(request.user, "pcn_number", "")),
        ("Email", request.user.email),
        ("Area of Practice", getattr(request.user, "area_of_practice", "")),
        ("Technical Group", clearance.get_technical_group_display() if clearance else ""),
        ("Clearance Year", clearance.clearance_year if clearance else ""),
    ]

    # Draw profile details with nice spacing
    y = current_y
    for label, value in profile_data:
        p.setFont("Helvetica-Bold", 13)
        p.setFillColor(colors.HexColor("#555"))
        p.drawString(left_margin, y, f"{label}:")
        p.setFont("Helvetica", 13)
        p.setFillColor(colors.HexColor("#2d6a4f"))
        p.drawString(left_margin + 200, y, str(value))
        y -= 28

    current_y = y - 40

    # ===== CLEARANCE STATUS =====
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.HexColor("#2d6a4f"))
    p.drawString(left_margin, current_y, "Clearance Status")
    current_y -= 30

    clearance_status = clearance.status if clearance else "Pending"
    clearance_comments = getattr(clearance, "comments", "Your application has been approved.")

    table_data = [
        ["Status", clearance_status],
        ["Comments", clearance_comments],
    ]

    table = Table(table_data, colWidths=[140, width - left_margin - right_margin - 140])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2d6a4f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor("#2d6a4f")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, left_margin, current_y - 70)

    # ===== FOOTER =====
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, 40,
                        "This document is valid without signature.")

    p.showPage()
    p.save()

    return response
    