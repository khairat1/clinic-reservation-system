from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from clinic.models import Department, Doctor, Schedule
from .models import Appointment
from .forms import AppointmentDateForm


# ─── STEP 1 — Choose Department ───────────────────────────────────────────────

@login_required
def booking_step1(request):
    departments = Department.objects.all()
    return render(request, 'appointments/step1.html', {
        'departments': departments
    })


# ─── STEP 2 — Choose Doctor ───────────────────────────────────────────────────

@login_required
def booking_step2(request):
    department_id = request.GET.get('department_id')
    if not department_id:
        return redirect('booking_step1')

    department = get_object_or_404(Department, pk=department_id)
    doctors = Doctor.objects.filter(department=department)

    request.session['department_id'] = department_id

    return render(request, 'appointments/step2.html', {
        'department': department,
        'doctors': doctors,
    })


# ─── STEP 3 — Choose Date ─────────────────────────────────────────────────────

@login_required
def booking_step3(request):
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return redirect('booking_step1')

    doctor = get_object_or_404(Doctor, pk=doctor_id)
    request.session['doctor_id'] = doctor_id
    form = AppointmentDateForm()

    return render(request, 'appointments/step3.html', {
        'doctor': doctor,
        'form': form,
    })


# ─── STEP 4 — Choose Time ─────────────────────────────────────────────────────

@login_required
def booking_step4(request):
    if request.method == 'POST':
        form = AppointmentDateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            request.session['date'] = str(selected_date)
        else:
            return redirect('booking_step3')
    else:
        return redirect('booking_step3')

    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('booking_step1')

    doctor = get_object_or_404(Doctor, pk=doctor_id)

    day_name = selected_date.strftime('%A')
    schedules = Schedule.objects.filter(doctor=doctor, day=day_name)

    booked_times = Appointment.objects.filter(
        doctor=doctor,
        date=selected_date
    ).values_list('time', flat=True)

    available_slots = []
    for schedule in schedules:
        from datetime import datetime, timedelta
        current = datetime.combine(selected_date, schedule.start_time)
        end     = datetime.combine(selected_date, schedule.end_time)
        while current < end:
            slot_time = current.time()
            if slot_time not in booked_times:
                available_slots.append(slot_time)
            current += timedelta(minutes=30)

    return render(request, 'appointments/step4.html', {
        'doctor': doctor,
        'selected_date': selected_date,
        'available_slots': available_slots,
    })


# ─── STEP 5 — Confirm & Save ──────────────────────────────────────────────────

@login_required
def booking_step5(request):
    if request.method == 'POST':
        time_str  = request.POST.get('time')
        doctor_id = request.session.get('doctor_id')
        date_str  = request.session.get('date')

        if not all([time_str, doctor_id, date_str]):
            return redirect('booking_step1')

        doctor = get_object_or_404(Doctor, pk=doctor_id)

        already_booked = Appointment.objects.filter(
            doctor=doctor,
            date=date_str,
            time=time_str,
        ).exists()

        if already_booked:
            messages.error(request, 'Sorry, this slot was just taken. Please choose another time.')
            return redirect('booking_step4')

        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date_str,
            time=time_str,
            status='confirmed',
        )

        request.session.pop('doctor_id', None)
        request.session.pop('department_id', None)
        request.session.pop('date', None)

        return render(request, 'appointments/step5.html', {
            'appointment': appointment,
        })

    return redirect('booking_step1')


# ─── MY APPOINTMENTS ──────────────────────────────────────────────────────────

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-date', '-time')

    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments,
    })


# ─── CANCEL APPOINTMENT ───────────────────────────────────────────────────────

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        patient=request.user
    )

    if appointment.status == 'confirmed':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Your appointment has been cancelled.')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')

    return redirect('my_appointments')
