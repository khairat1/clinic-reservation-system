from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Maymouna — clinic app (home, departments, doctors, public pages)
    path('', include('clinic.urls')),

    # Khairat — accounts app (register, login, logout)
    path('accounts/', include('accounts.urls')),
    
    
    
    
    # Bisan — appointments app (booking steps, my appointments, cancel)
    # Uncomment this when Bisan pushes her urls.py
    path('appointments/', include('appointments.urls')),
    
    # Mahmoud — chatbot app (chatbot interface)
    # Uncomment this when Mahmoud pushes his urls.py
    # path('chatbot/', include('chatbot.urls')),
]