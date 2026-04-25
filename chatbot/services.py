from clinic.models import Department
from groq import Groq

GROQ_API_KEY = "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"


def get_department_recommendation(symptom_text, chat_history=None):
    try:
        departments = Department.objects.all()
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
        print(f"Chatbot error: {e}")
        return {
            'found': False,
            'message': 'The AI assistant is temporarily unavailable. Please call the clinic directly.',
            'department': None,
        }


def handle_quick_action(action, department_name):
    from clinic.models import Doctor

    action = action.lower().strip()

    if 'find doctor' in action or 'doctor' in action:
        if department_name:
            try:
                doctors = Doctor.objects.filter(department__name__iexact=department_name)
                if doctors.exists():
                    names = ', '.join([d.name for d in doctors])
                    return {
                        'found': True,
                        'message': f'Here are the doctors available in the {department_name} department: {names}. You can book an appointment with any of them.',
                        'department': department_name,
                    }
            except:
                pass
        return {
            'found': False,
            'message': 'Please describe your symptoms first so I can find the right doctor for you.',
            'department': None,
        }

    if 'book' in action or 'appointment' in action:
        if department_name:
            try:
                doctors = Doctor.objects.filter(department__name__iexact=department_name)
                if doctors.exists():
                    names = ', '.join([d.name for d in doctors])
                    return {
                        'found': True,
                        'message': f'To book an appointment in the {department_name} department, you can choose from these doctors: {names}. Click "Book Appointment" in the sidebar to proceed.',
                        'department': department_name,
                        'redirect': '/appointments/',
                    }
            except:
                pass
        return {
            'found': False,
            'message': 'Please describe your symptoms first so I can recommend the right department before booking.',
            'department': None,
        }

    if 'department' in action:
        if department_name:
            try:
                department = Department.objects.get(name__iexact=department_name)
                return {
                    'found': True,
                    'message': f'You were referred to the {department.name} department. {department.description[:100]}... Click "Departments" in the sidebar to learn more.',
                    'department': department_name,
                    'redirect': '/clinic/departments/',
                }
            except:
                pass
        return {
            'found': False,
            'message': 'Please describe your symptoms first so I can direct you to the right department.',
            'department': None,
        }

    if 'contact' in action:
        return {
            'found': True,
            'message': 'You can reach MediClinic directly at: 📞 +90 212 555 0123. Our staff are available Monday to Friday, 8:00 AM to 6:00 PM.',
            'department': department_name,
        }

    return None