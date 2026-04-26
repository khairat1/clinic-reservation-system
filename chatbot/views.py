from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .services import get_department_recommendation, handle_quick_action
from .models import ChatHistory
import json
import uuid


def get_or_create_session(request):
    if 'chatbot_session_id' not in request.session:
        request.session['chatbot_session_id'] = str(uuid.uuid4())
        request.session.modified = True
    return request.session['chatbot_session_id']


@login_required
def chatbot_page(request):
    return render(request, 'chatbot/chatbot.html')


@login_required
def new_chat_view(request):
    request.session['chatbot_session_id'] = str(uuid.uuid4())
    request.session.modified = True
    return JsonResponse({'status': 'success', 'message': 'New conversation started.'})


@login_required
def chat_history_view(request):
    session_id = get_or_create_session(request)
    history = ChatHistory.objects.filter(
        user=request.user,
        session_id=session_id
    ).order_by('timestamp')

    data = [
        {
            'message': chat.message,
            'response': chat.response,
            'department': chat.department,
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M'),
        }
        for chat in history
    ]
    return JsonResponse({'history': data})


@login_required
@require_POST
def chatbot_view(request):
    session_id = get_or_create_session(request)
    
    # Handle both JSON and Form data
    try:
        if 'application/json' in (request.content_type or ''):
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            department_context = data.get('department', '').strip()
        else:
            user_message = request.POST.get('message', '').strip()
            department_context = request.POST.get('department', '').strip()
    except Exception as e:
        print(f"Chatbot view request error: {e}")
        user_message = ''
        department_context = ''

    if not user_message:
        return JsonResponse({'found': False, 'message': 'Please describe your symptoms.', 'department': None})

    # ─── BACKEND MEMORY FALLBACK ───
    # If frontend didn't send context, look it up in the current session history
    if not department_context:
        last_chat = ChatHistory.objects.filter(
            user=request.user,
            session_id=session_id,
            department__isnull=False
        ).exclude(department='').order_by('-timestamp').first()
        if last_chat:
            department_context = last_chat.department

    # Check for Quick Actions (Doctor search, booking, etc.)
    quick_result = handle_quick_action(user_message, department_context)
    if quick_result:
        # Update session with the last known department even for quick actions
        if department_context:
            quick_result['department'] = department_context
        return JsonResponse(quick_result)

    # Otherwise, it's a symptom search — get history for AI context
    chat_history = ChatHistory.objects.filter(
        user=request.user,
        session_id=session_id,
        department__isnull=False
    ).exclude(department='').order_by('-timestamp')[:5]
    chat_history = list(reversed(chat_history))

    # Get AI recommendation
    result = get_department_recommendation(user_message, chat_history)

    # Save to history
    ChatHistory.objects.create(
        user=request.user,
        session_id=session_id,
        message=user_message,
        response=result.get('message', 'Error'),
        department=result.get('department') or '',
    )

    return JsonResponse(result)