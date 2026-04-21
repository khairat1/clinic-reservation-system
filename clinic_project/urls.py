from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Temporary home view — replace this when Maymouna finishes clinic/urls.py
def temp_home(request):
    return HttpResponse("Home page coming soon.")

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Temporary home — remove this when Maymouna uncomments clinic.urls below
    path('', temp_home, name='home'),

    # Khairat — accounts app (register, login, logout)
    path('accounts/', include('accounts.urls')),
    
    # Maymouna — clinic app (home, departments, doctors, public pages)
    # Uncomment this when Maymouna pushes her urls.py
    # path('', include('clinic.urls')),
    
    # Bisan — appointments app (booking steps, my appointments, cancel)
    # Uncomment this when Bisan pushes her urls.py
    # path('appointments/', include('appointments.urls')),
    
    # Mahmoud — chatbot app (chatbot interface)
    # Uncomment this when Mahmoud pushes his urls.py
    # path('chatbot/', include('chatbot.urls')),
]