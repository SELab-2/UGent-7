from django.utils.translation import gettext as _

from authentication.models import User
from notifications.models import Notification, NotificationTemplate
from rest_framework import serializers


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    # Hyper linked user field
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        queryset=User.objects.all()
    )

    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_content(self, notification: Notification) -> str:
        """Get the content from the template and arguments."""
        return _(notification.template_id.description_key) % notification.arguments

    def get_title(self, notification: Notification) -> str:
        """Get the title from the template and arguments."""
        return _(notification.template_id.title_key)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "content",
            "title",
            "created_at",
            "is_read",
            "is_sent",
        ]
