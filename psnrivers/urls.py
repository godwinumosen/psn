from django.urls import path
from . import views
from .views import HomeView,NewsAndEventsView,UpcomingNewsAndEventsView
from .views import ArticleDetailView

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', HomeView.as_view(), name="home"),
    path('home/', HomeView.as_view(), name='home'),
    path('news_events/', NewsAndEventsView.as_view(), name='news_events'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name="detail"),
    path('upcoming_news_events/', UpcomingNewsAndEventsView.as_view(), name='upcoming_news_events'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path("about/who_we_are/", views.who_we_are, name="who_we_are"),
    path("about/aims/", views.aims, name="aims"),
    path("about/code/", views.code, name="code"),
    path("about/constitution/", views.constitution, name="constitution"),
    path("about/executive/", views.executive, name="executive"),
    path('directory/', views.directory, name='directory'),
    path('member_portal/', views.member_portal, name='member_portal'),
    path('clearance/', views.apply_clearance, name='clearance'),
    path('track_status/', views.track_status, name='track_status'),
    path('review_applications/', views.review_applications, name='review_applications'),
    path('review_applications/<int:app_id>/', views.application_detail, name='application_detail'),
    path('approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('decline/<int:app_id>/', views.decline_application, name='decline_application'),
    path("profile/", views.profile, name="profile"),
    path('profile/download/', views.profile_pdf, name='profile_pdf'),
    #path("success/", views.success, name="success"),
    # urls.py
    path("newsletter/subscribe/", views.subscribe_newsletter, name="newsletter_subscribe"),

    
]