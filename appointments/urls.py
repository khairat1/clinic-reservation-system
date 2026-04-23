from django.urls import path
from . import views

urlpatterns = [
    path('book/step1/', views.booking_step1, name='booking_step1'),
    path('book/step2/', views.booking_step2, name='booking_step2'),
    path('book/step3/', views.booking_step3, name='booking_step3'),
    path('book/step4/', views.booking_step4, name='booking_step4'),
    path('book/step5/', views.booking_step5, name='booking_step5'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]