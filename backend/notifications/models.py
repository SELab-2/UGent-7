from authentication.models import User
from django.db import models


class NotificationTemplate(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title_key = models.CharField(max_length=255)  # Key used to get translated title
    description_key = models.CharField(
        max_length=511
    )  # Key used to get translated description


class Notification(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template_id = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    arguments = models.JSONField(default=dict)  # Arguments to be used in the template
    is_read = models.BooleanField(
        default=False
    )  # Whether the notification has been read
    is_sent = models.BooleanField(
        default=False
    )  # Whether the notification has been sent (email)
