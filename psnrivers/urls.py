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
    
]