import re
from typing import Dict, List

from authentication.models import User
from notifications.logic import get_message_dict
from notifications.models import Notification, NotificationTemplate
from rest_framework import serializers


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    # Hyper linked user field
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail", queryset=User.objects.all()
    )

    # Translate template and arguments into a message
    message = serializers.SerializerMethodField()

    # Check if the required arguments are present
    def _get_missing_keys(self, string: str, arguments: Dict[str, str]) -> List[str]:
        required_keys: List[str] = re.findall(r"%\((\w+)\)", string)
        missing_keys = [key for key in required_keys if key not in arguments]

        return missing_keys

    def validate(self, data: Dict[str, str]) -> Dict[str, str]:
        data: Dict[str, str] = super().validate(data)

        # Validate the arguments
        if "arguments" not in data:
            data["arguments"] = {}

        title_missing = self._get_missing_keys(
            data["template_id"].title_key, data["arguments"]
        )
        description_missing = self._get_missing_keys(
            data["template_id"].description_key, data["arguments"]
        )

        if title_missing or description_missing:
            raise serializers.ValidationError(
                {
                    "missing arguments": {
                        "title": title_missing,
                        "description": description_missing,
                    }
                }
            )

        return data

    # Get the message from the template and arguments
    def get_message(self, obj: Notification) -> Dict[str, str]:
        return get_message_dict(obj)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "template_id",
            "arguments",
            "message",
            "created_at",
            "is_read",
            "is_sent",
        ]
