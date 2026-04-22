from django import forms
from .models import Department, Doctor, Schedule


class DepartmentForm(forms.ModelForm):
    class Meta:
        model  = Department
        fields = ['name', 'description', 'image']


class DoctorForm(forms.ModelForm):
    class Meta:
        model  = Doctor
        fields = ['name', 'department', 'description', 'image']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model  = Schedule
        fields = ['doctor', 'day', 'start_time', 'end_time']