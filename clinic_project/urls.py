from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Maymouna — clinic app (home, departments, doctors, public pages)
    path('', include('clinic.urls')),
    path('clinic/', include('clinic.urls')),

    # Khairat — accounts app (register, login, logout)
    path('accounts/', include('accounts.urls')),
    
    # Bisan — appointments app (booking steps, my appointments, cancel)
    path('appointments/', include('appointments.urls')),
    
    # Mahmoud — chatbot app (chatbot interface)
    path('chatbot/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)