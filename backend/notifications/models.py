from authentication.models import User
from django.db import models


class NotificationTemplate(models.Model):
    """This model represents a template for a notification."""
    id = models.AutoField(
        auto_created=True,
        primary_key=True
    )
    title_key = models.CharField(
        max_length=255
    )
    description_key = models.CharField(
        max_length=511
    )


class Notification(models.Model):
    """This model represents a notification."""
    id = models.AutoField(
        auto_created=True,
        primary_key=True
    )

    user = models.ForeignKey(
        User,
        related_name="notifications",
        on_delete=models.CASCADE
    )

    template_id = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    # Arguments to be used in the template
    arguments = models.JSONField(
        default=dict
    )
    # Whether the notification has been read
    is_read = models.BooleanField(
        default=False
    )
    # Whether the notification has been sent (email)
    is_sent = models.BooleanField(
        default=False
    )

    def sent(self):
        """Mark the notification as sent"""
        self.is_sent = True
        self.save()
