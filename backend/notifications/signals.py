from __future__ import annotations

from enum import Enum
from typing import Dict

from authentication.models import User
from django.dispatch import Signal, receiver
from django.urls import reverse
from notifications.serializers import NotificationSerializer

notification_create = Signal()


@receiver(notification_create)
def notification_creation(
    type: NotificationType, user: User, arguments: Dict[str, str], **kwargs
) -> bool:
    serializer = NotificationSerializer(
        data={
            "template_id": type.value,
            "user": reverse("user-detail", kwargs={"pk": user.id}),
            "arguments": arguments,
        }
    )

    if not serializer.is_valid():
        return False

    serializer.save()

    return True


class NotificationType(Enum):
    SCORE_ADDED = 1  # Arguments: {"score": int}
    SCORE_UPDATED = 2  # Arguments: {"score": int}
