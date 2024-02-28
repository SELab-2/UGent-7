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

    def get_message(self, obj):
        if obj.arguments != {}:
            return {
                "title": _(obj.template_id.title_key),
                "description": _(obj.template_id.description_key) % obj.arguments,
            }
        else:
            return {"title": "test", "description": "test2"}


# TODO: NotificationSerializer exclude = ['user'] and use depth = 1
# TODO: HyperlinkedModelSerializer?
# TODO: serializer method field as class?
# TODO: Error checking
