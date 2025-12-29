from django.urls import path
from . import views
#from .views import HomeView, ArticleDetailView,

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    
    
]