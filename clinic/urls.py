from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.home, name='home'),
    path('departments/', views.departments_list, name='departments_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('doctors/', views.doctors_list, name='doctors_list'),
]