from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('send/', views.chatbot_view, name='chatbot_send'),
    path('history/', views.chat_history_view, name='chat_history'),
]