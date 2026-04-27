# Online Medical Clinic Reservation System

## Project Demo

▶️ [Watch the full demo on YouTube](https://youtu.be/N1vMcbLirtg?si=vb7RC1I_c84_ANqo)

## Team Details
| Name | Student ID | GitHub Username |
|------|------------|-----------------|
| Khairat Joulak | 230513449 | khairat1 |
| Mahmoud Dib | 220513762 | mdib2602-bot |
| Abdulrahman Birecikli | 220513508 | A-jkjk |
| Maymouna Salameh | 230513607 | m4xn |
| Bisan Ibrahim | 220513038 | bisan7 |

## Project Introduction
A web-based platform for a medical complex that allows patients to register
and book appointments with doctors by selecting department, specialty, date,
and time. The system includes an AI chatbot assistant that guides patients
to the right department based on their symptoms.

## Architecture Link

[View Architecture Documentation](https://github.com/khairat1/clinic-reservation-system/blob/main/ARCHITECTURE.md)

## Prerequisites

- Python 3.10+
- PostgreSQL
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/khairat1/clinic-reservation-system.git
cd clinic-reservation-system
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL
Create a database named `clinic_db` with:
- User: `postgres`
- Password: `qwerty`
- Host: `localhost`
- Port: `5432`

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Load Initial Data
```bash
python manage.py loaddata clinic/fixtures/clinic_data.json
python manage.py loaddata clinic/fixtures/schedules_data.json
```

### 7. Generate Doctor and Department Icons
```bash
python generate_icons.py
```

### 8. Run the Server
```bash
python manage.py runserver
```

### 9. Access the Website
Open your browser and go to: http://127.0.0.1:8000

## Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | 230513449 | admin |

> To create your own admin account:
> ```bash
> python manage.py createsuperuser
> ```

## Key Pages

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Departments | http://127.0.0.1:8000/departments/ |
| Doctors | http://127.0.0.1:8000/doctors/ |
| Book Appointment | http://127.0.0.1:8000/appointments/book/step1/ |
| Chatbot | http://127.0.0.1:8000/chatbot/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |