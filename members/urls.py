from django.urls import path, reverse_lazy
from . import views
from .views import register, login_view, admin_dashboard, logout_view
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView

# Custom Password Reset Confirm View with success message
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'members/password_reset_confirm.html'
    success_url = reverse_lazy('members:login')  # ✅ include namespace

    def form_valid(self, form):
        messages.success(self.request, "Your password has been reset successfully. You can now log in.")
        return super().form_valid(form)


app_name = 'members'

urlpatterns = [
    # Public member pages under /members/
    path('register/', register, name='register'),
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('success/', views.success, name='success'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_email_view, name='resend_verification'),

    # Authentication URLs at root
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Password reset URLs at root
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='members/password_reset.html',
             email_template_name='members/password_reset_email.html',
             subject_template_name='members/password_reset_subject.txt',
             success_url=reverse_lazy('members:password_reset_done'),  
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='members/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='members/password_reset_complete.html'),
         name='password_reset_complete'),
]
