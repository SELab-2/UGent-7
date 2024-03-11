from __future__ import annotations

from enum import Enum
from typing import Dict, List, Union

from authentication.models import User
from django.db.models.query import QuerySet
from django.dispatch import Signal, receiver
from django.urls import reverse
from notifications.logic import schedule_send_mails
from notifications.serializers import NotificationSerializer

notification_create = Signal()


@receiver(notification_create)
def notification_creation(
    type: NotificationType,
    queryset: QuerySet[User],
    arguments: Dict[str, str],
    **kwargs,  # Required by django
) -> bool:
    data: List[Dict[str, Union[str, int, Dict[str, str]]]] = []

    for user in queryset:
        data.append(
            {
                "template_id": type.value,
                "user": reverse("user-detail", kwargs={"pk": user.id}),
                "arguments": arguments,
            }
        )

    serializer = NotificationSerializer(data=data, many=True)

    if not serializer.is_valid():
        return False

    serializer.save()

    schedule_send_mails()

    return True


class NotificationType(Enum):
    SCORE_ADDED = 1  # Arguments: {"score": int}
    SCORE_UPDATED = 2  # Arguments: {"score": int}
