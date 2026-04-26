from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),
    path('send/', views.chatbot_view, name='chatbot_send'),
    path('history/', views.chat_history_view, name='chat_history'),
    path('new-chat/', views.new_chat_view, name='new_chat'),
]