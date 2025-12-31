from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import User
from django.db.models import Count
from django.utils.timezone import now

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            messages.success(request, "Registration successful. Await approval.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'members/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if user.status == 'approved':
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Account pending approval.")
        else:
            messages.error(request, "Invalid login details.")
    return render(request, 'members/login.html')

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
