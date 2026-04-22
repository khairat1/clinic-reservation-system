from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Department, Doctor
from .forms import DepartmentForm, DoctorForm


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


# ─── ADMIN VIEWS ─────────────────────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('clinic:home')
    departments = Department.objects.all()
    doctors     = Doctor.objects.all()
    return render(request, 'clinic/admin_dashboard.html', {
        'departments': departments,
        'doctors':     doctors,
    })


@login_required
def add_department(request):
    if request.user.role != 'admin':
        return redirect('clinic:home')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinic:admin_dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'clinic/add_department.html', {'form': form})


@login_required
def edit_department(request, pk):
    if request.user.role != 'admin':
        return redirect('clinic:home')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('clinic:admin_dashboard')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'clinic/edit_department.html', {
        'form':       form,
        'department': department,
    })


@login_required
def add_doctor(request):
    if request.user.role != 'admin':
        return redirect('clinic:home')
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinic:admin_dashboard')
    else:
        form = DoctorForm()
    return render(request, 'clinic/add_doctor.html', {'form': form})


@login_required
def edit_doctor(request, pk):
    if request.user.role != 'admin':
        return redirect('clinic:home')
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('clinic:admin_dashboard')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'clinic/edit_doctor.html', {
        'form':   form,
        'doctor': doctor,
    })