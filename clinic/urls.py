from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('departments/', views.departments_list, name='departments_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),

    # Admin management pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add-department/', views.add_department, name='add_department'),
    path('admin-dashboard/edit-department/<int:pk>/', views.edit_department, name='edit_department'),
    path('admin-dashboard/add-doctor/', views.add_doctor, name='add_doctor'),
    path('admin-dashboard/edit-doctor/<int:pk>/', views.edit_doctor, name='edit_doctor'),
]