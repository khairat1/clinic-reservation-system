from django.db import models


class Department(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    image       = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name        = models.CharField(max_length=100)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    description = models.TextField()
    image       = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAYS = [
        ('Monday',    'Monday'),
        ('Tuesday',   'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday',  'Thursday'),
        ('Friday',    'Friday'),
        ('Saturday',  'Saturday'),
        ('Sunday',    'Sunday'),
    ]

    doctor     = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day        = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time   = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} — {self.day} {self.start_time} to {self.end_time}"