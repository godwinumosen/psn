from django.urls import path
from . import views
from .views import HomeView, ExcosUserPage

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('home/', HomeView.as_view(), name='home'),
    path('whoweare/', views.whoWeAre, name='whoweare'),
    path('whatwedo/', views.whatWeDo, name='whatwedo'),
    path('whypsn/', views.WhyPsn, name='whypsn'),
    path('ourimpact/', views.OurImpact, name='ourimpact'),
    path('contact_us/', views.Contact_Us, name='contact_us'),
    path('dala2025/', views.Dala2025, name='dala2025'),
    # Updated URL to accept email as parameter
    path('excos_user/', ExcosUserPage.as_view(), name='excos_user'),  # List all users
    path('excos_user/<str:email>/', ExcosUserPage.as_view(), name='excos_user')
]
