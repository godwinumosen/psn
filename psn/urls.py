from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root-level auth URLs
    path('', include('members.urls')),  # Login, logout, password reset

    # All other member URLs under /members/
    path('members/', include(('members.urls', 'members'), namespace='members')),

    # Your main app URLs
    path('', include('psnrivers.urls')),
]

# Custom Admin Titles
admin.site.site_header = "psnrivers Admin"
admin.site.site_title = "psnrivers"

# Serve media and static in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
