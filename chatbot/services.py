from clinic.models import Department
from django.conf import settings
from groq import Groq

GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', '')


def get_department_recommendation(symptom_text, chat_history=None):
    try:
        departments = Department.objects.all()
        if not departments.exists():
            dept_list = "General Medicine, Cardiology, Neurology, Pediatrics"
        else:
            dept_names = [d.name for d in departments]
            dept_list = ', '.join(dept_names)

        messages = [
            {
                "role": "system",
                "content": f"""You are a medical assistant chatbot for MediClinic.
The clinic has these departments: {dept_list}.

Rules:
- If the message is not a clear medical symptom (random letters, greetings, vague words, nonsense), reply ONLY with:
DEPARTMENT: NONE
REASON: Please describe your symptoms clearly so I can help you.

- If the message contains a real medical symptom, reply with:
DEPARTMENT: <department name>
REASON: <one short specific sentence explaining why>

- Remember the entire conversation history
- Never recommend a department unless the patient clearly describes a medical symptom
- Only use department names from this list: {dept_list}"""
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
        reason = None

        for line in ai_response.split('\n'):
            if line.startswith('DEPARTMENT:'):
                department_name = line.replace('DEPARTMENT:', '').strip()
            if line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()

        if department_name and department_name.upper() == 'NONE':
            return {
                'found': False,
                'message': reason or 'Please describe your symptoms clearly so I can help you.',
                'department': None,
            }

        if department_name:
            department = Department.objects.filter(name__iexact=department_name).first()
            if department:
                return {
                    'found': True,
                    'message': f'Based on your symptoms, we recommend the {department.name} department. {reason}',
                    'department': department.name,
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