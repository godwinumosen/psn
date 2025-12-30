from django.urls import path
from . import views
#from .views import HomeView, ArticleDetailView,

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('news_events/', views.news_events, name='news_events'),
    
    
]