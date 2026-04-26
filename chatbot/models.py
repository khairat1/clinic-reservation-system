from django.db import models
from django.conf import settings


class ChatHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    session_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    message = models.TextField()
    response = models.TextField()
    department = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']