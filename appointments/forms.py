from django import forms
from django.utils import timezone


class AppointmentDateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': str(timezone.now().date()),
        }),
        label='Select Date'
    )