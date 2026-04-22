from django.shortcuts import render, get_object_or_404
from .models import Department, Doctor


def home(request):
    departments = Department.objects.all()
    doctors     = Doctor.objects.all()
    return render(request, 'clinic/home.html', {
        'departments': departments,
        'doctors':     doctors,
    })


def departments_list(request):
    departments = Department.objects.all()
    return render(request, 'clinic/departments.html', {
        'departments': departments,
    })


def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    doctors    = Doctor.objects.filter(department=department)
    return render(request, 'clinic/department_detail.html', {
        'department': department,
        'doctors':    doctors,
    })


def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic/doctors_list.html', {
        'doctors': doctors,
    })