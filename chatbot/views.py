import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import get_department_recommendation
from .models import ChatHistory

@login_required
def chatbot_page(request):
    return render(request, 'chatbot/chatbot.html')


@login_required
@require_POST
def chatbot_view(request):
    if request.content_type == 'application/json':
        try:
            body = json.loads(request.body)
            user_message = body.get('message', '').strip()
        except json.JSONDecodeError:
            user_message = ''
    else:
        user_message = request.POST.get('message', '').strip()

    if not user_message:
        return JsonResponse({
            'found': False,
            'message': 'Please enter your symptoms.',
            'department': None,
        })

    # Call services.py — all AI logic lives there
    result = get_department_recommendation(user_message)

    # Save the conversation to the database
    ChatHistory.objects.create(
        user=request.user,
        message=user_message,
        response=result['message'],
    )

    return JsonResponse(result)


@login_required
def chat_history_view(request):
    history = ChatHistory.objects.filter(user=request.user)
    
    data = []
    for chat in history:
        data.append({
            'id': chat.id,
            'message': chat.message,
            'response': chat.response,
            'timestamp': chat.timestamp.isoformat(),
        })
        
    return JsonResponse({'history': data})