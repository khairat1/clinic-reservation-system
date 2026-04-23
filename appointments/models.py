
from django.db import models
from django.contrib.auth import get_user_model
from clinic.models import Doctor

User = get_user_model()

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor     = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date       = models.DateField()
    time       = models.TimeField()
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.patient.username} → {self.doctor.name} on {self.date} at {self.time}"