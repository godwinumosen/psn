from django.urls import path
from . import views
from .views import HomeView, ArticleDetailView,NewsAndEventsView

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', HomeView.as_view(), name="home"),
    path('home/', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name="detail"),
    path('news_events/', NewsAndEventsView.as_view(), name='news_events'),
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
    
]