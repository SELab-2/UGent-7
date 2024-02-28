import re
from typing import Dict, List

from django.utils.translation import gettext as _
from notifications.models import Notification, NotificationTemplate
from rest_framework import serializers


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

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

    def _get_missing_keys(self, s: str, d: Dict[str, str]) -> List[str]:
        required_keys = re.findall(r"%\((\w+)\)", s)
        missing_keys = [key for key in required_keys if key not in d]

        return missing_keys

    def validate(self, data):
        data = super().validate(data)

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

    def get_message(self, obj):
        return {
            "title": _(obj.template_id.title_key),
            "description": _(obj.template_id.description_key) % obj.arguments,
        }


# TODO: HyperlinkedModelSerializer
