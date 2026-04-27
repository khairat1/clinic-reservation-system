from clinic.models import Department
from django.conf import settings
from groq import Groq

GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', '')

# Doctor specializations for AI context
DOCTOR_SPECIALIZATIONS = {
    "Dr. Ahmed Al-Rashid":  "Interventional Cardiologist — coronary artery disease, angioplasty, stenting",
    "Dr. Sarah Mitchell":   "Cardiac Electrophysiologist — heart rhythm disorders, atrial fibrillation, ablation",
    "Dr. Omar Yıldız":      "Heart Failure Specialist — advanced heart failure, cardiac rehabilitation, preventive cardiology",
    "Dr. Layla Hassan":     "Stroke Neurologist — stroke management, cerebrovascular disease, post-stroke rehabilitation",
    "Dr. James Carter":     "Epilepsy Specialist — epilepsy, EEG, drug-resistant seizures",
    "Dr. Fatima Al-Zahra":  "Movement Disorders Specialist — Parkinson's disease, tremor, dystonia, Deep Brain Stimulation",
    "Dr. Emily Chen":       "General Pediatrician — routine child care, vaccinations, developmental screening",
    "Dr. Hassan Al-Amin":   "Pediatric Cardiologist — congenital heart defects, cardiac disease in children",
    "Dr. Sophia Müller":    "Neonatal Specialist — premature babies, critically ill newborns, neonatal intensive care",
    "Dr. Anna Kowalski":    "Internal Medicine Specialist — complex adult conditions, chronic disease management",
    "Dr. Mehmet Kaya":      "Family Medicine Physician — preventive care, health education, all ages",
    "Dr. Rachel Green":     "Geriatrician — elderly care, dementia, osteoporosis, falls prevention",
}


def get_department_recommendation(symptom_text, chat_history=None):
    try:
        departments = Department.objects.all()
        if not departments.exists():
            dept_list = "General Medicine, Cardiology, Neurology, Pediatrics"
        else:
            dept_names = [d.name for d in departments]
            dept_list = ', '.join(dept_names)

        # Build doctor list string for AI
        doctor_list = '\n'.join([f"- {name}: {spec}" for name, spec in DOCTOR_SPECIALIZATIONS.items()])

        messages = [
            {
                "role": "system",
                "content": f"""You are a medical assistant chatbot for MediClinic.

The clinic has these departments: {dept_list}.

The clinic has these doctors and their specializations:
{doctor_list}

Rules:
- If the message is not a clear medical symptom (random letters, greetings, vague words, nonsense), reply ONLY with:
DEPARTMENT: NONE
DOCTOR: NONE
REASON: Please describe your symptoms clearly so I can help you.

- If the message contains a real medical symptom, reply with:
DEPARTMENT: <department name from the list>
DOCTOR: <most suitable doctor name from the list>
REASON: <one short specific sentence explaining why this doctor is the best match>

- Always recommend the most specific specialist that matches the symptom
- Only use department names from this list: {dept_list}
- Only use doctor names from the doctor list above
- Never recommend a department or doctor unless the patient clearly describes a medical symptom
- Remember the entire conversation history"""
            }
        ]

        if chat_history:
            for chat in chat_history:
                messages.append({"role": "user", "content": chat.message})
                messages.append({"role": "assistant", "content": chat.response})

        messages.append({"role": "user", "content": symptom_text})

        client = Groq(api_key=GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )

        ai_response = chat_completion.choices[0].message.content.strip()

        department_name = None
        doctor_name = None
        reason = None

        for line in ai_response.split('\n'):
            if line.startswith('DEPARTMENT:'):
                department_name = line.replace('DEPARTMENT:', '').strip()
            if line.startswith('DOCTOR:'):
                doctor_name = line.replace('DOCTOR:', '').strip()
            if line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()

        if department_name and department_name.upper() == 'NONE':
            return {
                'found': False,
                'message': reason or 'Please describe your symptoms clearly so I can help you.',
                'department': None,
            }

        if department_name:
            from clinic.models import Doctor
            department = Department.objects.filter(name__iexact=department_name).first()

            if department:
                # Try to find the specific recommended doctor
                doctor = None
                if doctor_name and doctor_name.upper() != 'NONE':
                    doctor = Doctor.objects.filter(
                        name__iexact=doctor_name,
                        department=department
                    ).first()
                    if not doctor:
                        # Fuzzy match
                        doctor = Doctor.objects.filter(
                            name__icontains=doctor_name.split('.')[-1].strip(),
                            department=department
                        ).first()

                if doctor:
                    doctor_link = f'<a href="/doctors/{doctor.id}/" style="color: #0b50c4; font-weight: bold; text-decoration: underline;">{doctor.name}</a>'
                    book_link = f'<a href="/appointments/book/step3/?doctor_id={doctor.id}" style="color: white; background: #0b50c4; padding: 4px 12px; border-radius: 6px; text-decoration: none; font-weight: bold;">Book Appointment</a>'
                    message = (
                        f'Based on your symptoms, we recommend the <strong>{department.name}</strong> department. '
                        f'{reason}<br><br>'
                        f'The best specialist for your condition is {doctor_link}. '
                        f'<br><br>{book_link}'
                    )
                else:
                    message = (
                        f'Based on your symptoms, we recommend the <strong>{department.name}</strong> department. '
                        f'{reason}'
                    )

                return {
                    'found': True,
                    'message': message,
                    'department': department.name,
                    'doctor_id': doctor.id if doctor else None,
                }

        return {
            'found': False,
            'message': 'I could not identify a department. Please describe your symptoms more clearly.',
            'department': None,
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Chatbot error: {e}")
        return {
            'found': False,
            'message': 'The AI assistant is temporarily unavailable. Please call the clinic directly.',
            'department': None,
        }


def handle_quick_action(action, department_name):
    from clinic.models import Doctor, Department

    action = action.lower().strip()

    target_dept = None
    if department_name:
        target_dept = Department.objects.filter(name__iexact=department_name).first()
        if not target_dept:
            target_dept = Department.objects.filter(name__icontains=department_name).first()

    if 'find doctor' in action or 'doctor' in action:
        if target_dept:
            doctors = Doctor.objects.filter(department=target_dept)
            if doctors.exists():
                links = []
                for d in doctors:
                    links.append(f'<a href="/doctors/{d.id}/" style="color: #0b50c4; font-weight: bold; text-decoration: underline;">{d.name}</a>')
                names_html = ', '.join(links)
                return {
                    'found': True,
                    'message': f'Here are the specialists in our {target_dept.name} department: {names_html}. They are ready to help you.',
                    'department': target_dept.name,
                }
        return {
            'found': False,
            'message': 'Please describe your symptoms first so I can find the most relevant doctor for you.',
            'department': None,
        }

    if 'book' in action or 'appointment' in action:
        if target_dept:
            doctors = Doctor.objects.filter(department=target_dept)
            if doctors.exists():
                links = [f'<a href="/doctors/{d.id}/" style="color: #0b50c4; font-weight: bold; text-decoration: underline;">{d.name}</a>' for d in doctors]
                names_html = ', '.join(links)
            else:
                names_html = 'our specialists'
            return {
                'found': True,
                'message': f'To book an appointment in the {target_dept.name} department, you can choose from these doctors: {names_html}. You can click "Book Appointment" in the sidebar when you are ready to proceed.',
                'department': target_dept.name,
            }
        return {
            'found': False,
            'message': 'Please describe your symptoms first so I can guide you to the correct department for booking.',
            'department': None,
        }

    if 'department' in action:
        if target_dept:
            description_snippet = (target_dept.description or '')[:120]
            return {
                'found': True,
                'message': f'You were referred to the {target_dept.name} department. {description_snippet}... You can learn more by clicking "Departments" in the sidebar.',
                'department': target_dept.name,
            }
        return {
            'found': False,
            'message': 'Tell me a bit about your symptoms, and I will show you the right department.',
            'department': None,
        }

    if 'contact' in action:
        return {
            'found': True,
            'message': 'You can reach MediClinic at: 📞 +90 212 555 0123. We are here to help!',
            'department': department_name,
        }

    return None