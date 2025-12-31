from django.urls import path
from .views import register, login_view, admin_dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', admin_dashboard, name='dashboard'),
]
