from django.contrib import admin
from .models import ChatHistory


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'message', 'response']
    search_fields = ['user__username', 'message']
    readonly_fields = ['user', 'message', 'response', 'timestamp']
    ordering = ['-timestamp']