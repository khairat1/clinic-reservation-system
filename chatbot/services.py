from clinic.models import Department
from groq import Groq
from django.conf import settings

def get_department_recommendation(symptom_text):
    try:
        # Get all real department names from the database
        departments = Department.objects.all()
        dept_names = [d.name for d in departments]
        dept_list = ', '.join(dept_names)

        # Build the prompt
        prompt = f"""You are a medical assistant for a clinic. 
The clinic has these departments: {dept_list}.

A patient describes their symptoms: "{symptom_text}"

Your job:
1. Read the symptoms carefully
2. Decide which ONE department best matches
3. Reply in exactly this format and nothing else:
DEPARTMENT: <department name>
REASON: <one sentence explanation>

Only use department names from this list: {dept_list}"""

        # Call Groq AI
        client = Groq(api_key=settings.GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        ai_response = chat_completion.choices[0].message.content.strip()

        # Parse the AI response
        department_name = None
        reason = None

        for line in ai_response.split('\n'):
            if line.startswith('DEPARTMENT:'):
                department_name = line.replace('DEPARTMENT:', '').strip()
            if line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()

        # Verify the department exists in the database
        if department_name:
            department = Department.objects.filter(name__iexact=department_name).first()
            if department:
                return {
                    'found': True,
                    'message': f'Based on your symptoms, we recommend the {department.name} department. {reason}',
                    'department': department.name,
                }

        # Fallback if parsing failed
        return {
            'found': False,
            'message': 'I could not identify a department. Please visit General Medicine or call the clinic directly.',
            'department': None,
        }

    except Exception as e:
        return {
            'found': False,
            'message': 'The AI assistant is temporarily unavailable. Please call the clinic directly.',
            'department': None,
        }