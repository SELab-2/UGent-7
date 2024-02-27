from authentication.models import User
from django.db import models


class NotificationTemplate(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title_key = models.CharField(required=True, max_length=255)
    description_key = models.CharField(required=True, max_length=255)


class Notification(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, required=True, on_delete=models.CASCADE)
    template = models.ForeignKey(NotificationTemplate, required=True, on_delete=models.CASCADE, db_column='template_id')
    created_at = models.DateTimeField(auto_now_add=True)
    arguments = models.JSONField(required=False, default=dict)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
