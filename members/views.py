from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
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
from django.contrib import messages
from .models import User


def resend_verification_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        try:
            user = User.objects.get(email__iexact=email)
            if user.email_verified:
                messages.info(request, "Your email is already verified. You can log in.")
            else:
                send_verification_email(user, request)
                messages.success(request, "Verification email resent. Check your inbox.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return redirect("login")



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            # Find the user by email (case-insensitive)
            user_obj = User.objects.get(email__iexact=email)

            # Authenticate using email directly
            user = authenticate(request, email=email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if not user.email_verified:
                # ✅ Just show a warning, don't resend automatically
                messages.warning(
                    request, 
                    "Please verify your email before logging in. "
                    "Check the email we sent you after registration."
                )
                return redirect('login')

            if user.is_active:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')  # replace with your dashboard URL
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
        return redirect('login')
    else:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('login')


def success (request):
    return render (request, 'members/success.html')


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
        return redirect('login')

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


