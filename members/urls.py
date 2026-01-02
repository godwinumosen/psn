from django.urls import path
from . import views
from .views import register, login_view, admin_dashboard,logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('success/', views.success, name='success'),
    path('dashboard/', admin_dashboard, name='dashboard'),
]
