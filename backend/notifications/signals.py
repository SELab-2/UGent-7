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
    sender: type,
    type: NotificationType,
    queryset: list[User],
    arguments: Dict[str, str],
    **kwargs,  # Required by django
) -> bool:
    data: List[Dict[str, Union[str, int, Dict[str, str]]]] = []

    for user in queryset:
        if user:
            data.append(
                {
                    "template_id": type.value,
                    "user": reverse("user-detail", kwargs={"pk": user.id}),
                    "arguments": arguments,
                }
            )

    serializer = NotificationSerializer(data=data, many=True)

    if not serializer.is_valid(raise_exception=False):
        return False

    serializer.save()

    schedule_send_mails()

    return True


class NotificationType(Enum):
    SCORE_ADDED = 1  # Arguments: {"score": int}
    SCORE_UPDATED = 2  # Arguments: {"score": int}
    DOCKER_IMAGE_BUILD_SUCCESS = 3  # Arguments: {"name": str}
    DOCKER_IMAGE_BUILD_ERROR = 4  # Arguments: {"name": str}
    EXTRA_CHECK_SUCCESS = 5  # Arguments: {"name": str}
    EXTRA_CHECK_FAIL = 6  # Arguments: {"name": str}
    STRUCTURE_CHECK_SUCCESS = 7  # Arguments: {}
    STRUCTURE_CHECK_FAIL = 8  # Arguments: {}
    SUBMISSION_RECEIVED = 9  # Arguments: {}
