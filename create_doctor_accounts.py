"""
create_doctor_accounts.py
--------------------------
Run this script from the root of your Django project:
    python create_doctor_accounts.py

What it does:
- Creates a user account for each doctor
- Sets role to 'doctor'
- Links the user to the Doctor profile
- Prints username and password for each doctor
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_project.settings')
django.setup()

from clinic.models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()

# Doctor accounts — username and password for each
doctor_accounts = [
    {"doctor_name": "Dr. Ahmed Al-Rashid",  "username": "dr.ahmed",    "password": "Doctor1234"},
    {"doctor_name": "Dr. Sarah Mitchell",   "username": "dr.sarah",    "password": "Doctor1234"},
    {"doctor_name": "Dr. Omar Yıldız",      "username": "dr.omar",     "password": "Doctor1234"},
    {"doctor_name": "Dr. Layla Hassan",     "username": "dr.layla",    "password": "Doctor1234"},
    {"doctor_name": "Dr. James Carter",     "username": "dr.james",    "password": "Doctor1234"},
    {"doctor_name": "Dr. Fatima Al-Zahra",  "username": "dr.fatima",   "password": "Doctor1234"},
    {"doctor_name": "Dr. Emily Chen",       "username": "dr.emily",    "password": "Doctor1234"},
    {"doctor_name": "Dr. Hassan Al-Amin",   "username": "dr.hassan",   "password": "Doctor1234"},
    {"doctor_name": "Dr. Sophia Müller",    "username": "dr.sophia",   "password": "Doctor1234"},
    {"doctor_name": "Dr. Anna Kowalski",    "username": "dr.anna",     "password": "Doctor1234"},
    {"doctor_name": "Dr. Mehmet Kaya",      "username": "dr.mehmet",   "password": "Doctor1234"},
    {"doctor_name": "Dr. Rachel Green",     "username": "dr.rachel",   "password": "Doctor1234"},
]

print("Creating doctor accounts...\n")

for entry in doctor_accounts:
    # Check if user already exists
    if User.objects.filter(username=entry["username"]).exists():
        print(f"  ⚠️  User '{entry['username']}' already exists — skipping.")
        continue

    # Create user
    user = User.objects.create_user(
        username=entry["username"],
        password=entry["password"],
        role="doctor"
    )

    # Link to Doctor profile
    try:
        doctor = Doctor.objects.get(name=entry["doctor_name"])
        doctor.user = user
        doctor.save()
        print(f"  ✅  {entry['doctor_name']} → username: {entry['username']} | password: {entry['password']}")
    except Doctor.DoesNotExist:
        print(f"  ❌  Doctor '{entry['doctor_name']}' not found in database — user created but not linked.")

print("\nDone! All doctor accounts created.")
print("\nAll doctors share the same password: Doctor1234")
print("They can change it after first login via the admin panel.")
