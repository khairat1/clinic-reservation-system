from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .services import get_department_recommendation, handle_quick_action
from .models import ChatHistory
import json


@login_required
def chatbot_page(request):
    return render(request, 'chatbot/chat.html')


@login_required
def chat_history_view(request):
    history = ChatHistory.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:20]

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


@csrf_exempt
@login_required
@require_POST
def chatbot_view(request):
    # Handle both JSON and Form data
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            department_context = data.get('department', '').strip()
        except json.JSONDecodeError:
            user_message = ''
            department_context = ''
    else:
        user_message = request.POST.get('message', '').strip()
        department_context = request.POST.get('department', '').strip()

    if not user_message:
        return JsonResponse({
            'found': False,
            'message': 'Please describe your symptoms so I can help you.',
            'department': None,
        })

    # Get last 10 real symptom conversations only
    chat_history = ChatHistory.objects.filter(
        user=request.user,
        department__isnull=False
    ).exclude(
        department=''
    ).order_by('-timestamp')[:10]
    chat_history = list(reversed(chat_history))

    # Get last department from history if not sent
    if not department_context:
        for chat in reversed(chat_history):
            if chat.department:
                department_context = chat.department
                break

    # Check if this is a quick action button
    quick_result = handle_quick_action(user_message, department_context)
    if quick_result:
        # Don't save quick actions to history — only save real symptoms
        return JsonResponse(quick_result)

    # Otherwise treat as symptoms — pass full history to AI
    result = get_department_recommendation(user_message, chat_history)

    ChatHistory.objects.create(
        user=request.user,
        message=user_message,
        response=result['message'],
        department=result.get('department') or '',
    )

    return JsonResponse(result)