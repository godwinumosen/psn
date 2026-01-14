from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count
from django.utils.timezone import now
from .utils import send_verification_email
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib import messages
from .models import User



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'members/password_reset_confirm.html'
    success_url = reverse_lazy('members:login')  # ✅ now this works with namespace

    def form_valid(self, form):
        messages.success(self.request, "Your password has been reset successfully. You can now log in.")
        return super().form_valid(form)
    
    
    

def resend_verification_email_view(request):
    if request.method == "POST":
        # Get email from form and clean it
        email = request.POST.get("email", "").lower().strip()

        if not email:
            messages.error(request, "Please enter your email to resend verification.")
            return redirect("members:login")

        try:
            user = User.objects.get(email__iexact=email)

            if user.email_verified:
                # Already verified
                messages.info(request, "Your email is already verified. You can log in.")
            else:
                # Make sure user has a token
                if not hasattr(user, "email_verification_token") or not user.email_verification_token:
                    # Generate a new token if missing
                    user.email_verification_token = User.objects.make_random_password(length=64)
                    user.save()

                # Send verification email
                try:
                    send_verification_email(user, request)
                    messages.success(request, "Verification email resent. Check your inbox.")
                except Exception as e:
                    # Fail gracefully if email sending fails
                    messages.error(request, f"Failed to send verification email. Please try again later. ({e})")

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return redirect("members:login")





def login_view(request):
    if request.method == 'POST':
        # Check which action was submitted
        action = request.POST.get('action', 'login')  # default to login

        email = request.POST.get('email')
        if email:
            email = email.lower()
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user_obj = None

        if action == 'resend_verification':
            # Handle Resend Verification
            if user_obj:
                if user_obj.email_verified:
                    messages.info(request, "Your email is already verified. You can log in.")
                else:
                    # Send verification email (replace with your email function)
                    try:
                        # Example: send_mail(subject, message, from_email, [to_email])
                        verification_link = f"http://yourdomain.com/verify_email/{user_obj.email_verification_token}/"
                        send_mail(
                            subject="Verify Your Email",
                            message=f"Click the link to verify your email: {verification_link}",
                            from_email="noreply@psnriversstate.com",
                            recipient_list=[user_obj.email],
                        )
                        messages.success(request, "Verification email resent. Please check your inbox.")
                    except Exception as e:
                        messages.error(request, f"Failed to send email. Please try again later. ({e})")
            else:
                messages.error(request, "Email not found. Please register first.")

            return redirect('members:login')

        # Default login flow
        if user_obj:
            user = authenticate(request, email=email, password=password)
        else:
            user = None

        if user is not None:
            if not user.email_verified:
                messages.warning(
                    request, 
                    "Please verify your email before logging in. "
                    "Check the email we sent you after registration."
                )
                return redirect('members:login')

            if user.is_active:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('member_portal')
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'members/login.html')





def verify_email(request, uidb64, token):
    """
    Verify the user's email using UID and token.
    """
    try:
        # Decode UID from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    # Check token
    if user is not None and default_token_generator.check_token(user, token):
        # ✅ Mark email as verified
        user.email_verified = True
        user.save()

        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect('members:login')
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('members:login')


def success(request):
    return render(request, 'members/success.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Ensure email is lowercase
            user.email = user.email.lower()
            
            # Set username to lowercase email
            user.username = user.email
            
            # Hash password correctly
            user.set_password(form.cleaned_data['password1'])
            
            # Keep admin approval system
            user.is_active = True
            user.status = 'pending'  # or 'approved' if you auto-approve
            
            # Save area_of_practice explicitly from form
            user.area_of_practice = form.cleaned_data.get('area_of_practice')
            
            # Save user
            user.save()
            
            # Send verification email
            send_verification_email(user, request)
            
            messages.success(request, "Registration successful. Check your email to verify your account.")
            
            return render(request, 'members/success.html', {'user': user})
    else:
        form = RegistrationForm()
    
    return render(request, 'members/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('members:login')

    total_members = User.objects.count()
    pending_members = User.objects.filter(status='pending').count()
    approved_members = User.objects.filter(status='approved').count()
    rejected_members = User.objects.filter(status='rejected').count()
    paid_members = User.objects.filter(payment_status=True).count()
    unpaid_members = User.objects.filter(payment_status=False).count()

    practice_data = User.objects.values('area_of_practice').annotate(total=Count('id'))
    category_data = User.objects.values('membership_category').annotate(total=Count('id'))

    current_year = now().year
    monthly_data = (
        User.objects
        .filter(date_joined__year=current_year)
        .extra(select={'month': "strftime('%%m', date_joined)"})
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    context = {
        'total_members': total_members,
        'pending_members': pending_members,
        'approved_members': approved_members,
        'rejected_members': rejected_members,
        'paid_members': paid_members,
        'unpaid_members': unpaid_members,
        'practice_data': practice_data,
        'category_data': category_data,
        'monthly_data': monthly_data,
    }
    return render(request, 'members/admin_dashboard.html', context)
