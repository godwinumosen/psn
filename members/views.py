from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import User
from django.db.models import Count
from django.utils.timezone import now
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            # Find the user by email (case-insensitive)
            user_obj = User.objects.get(email__iexact=email)

            # Authenticate using email directly (works for your custom User model)
            user = authenticate(request, email=email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if user.is_active:  # Allow login immediately, no 'approved' check
                login(request, user)
                
                # ✅ Add success message
                messages.success(request, "Login successful.")
                
                return redirect('home')  # replace with your dashboard URL
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'members/login.html')




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
            
            user.save()
            
            messages.success(request, "Registration successful. Await approval.")
            
            # Render success page with user info
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


