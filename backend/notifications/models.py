from authentication.models import User
from django.db import models


class NotificationTemplate(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title_key = models.CharField(required=True, max_length=255)
    description_key = models.CharField(required=True, max_length=255)


class Notification(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, required=True, on_delete=models.CASCADE)
    template_id = models.ForeignKey(NotificationTemplate, required=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    arguments = models.JSONField(required=False, default=dict)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    def read(self):
        self.is_read = True
        self.save()

    def send(self):
        self.is_sent = True
        self.save()
