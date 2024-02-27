from django.utils.translation import gettext as _
from notifications.models import Notification, NotificationTemplate
from rest_framework import serializers


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, lookup_field="pk"
    )
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        exclude = ["template_id"]

    def get_title(self, obj):
        return _(NotificationTemplate.objects.get(pk=obj.template_id).title_key)

    def get_description(self, obj):
        description_key = NotificationTemplate.objects.get(
            pk=obj.template_id
        ).description_key

        return _(description_key).format(**obj.arguments)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data["template_id"] = {
    #         "title_key": NotificationTemplate.objects.get(
    #             pk=instance.template_id
    #         ).title_key,
    #         "description_key": NotificationTemplate.objects.get(
    #             pk=instance.template_id
    #         ).description_key,
    #     }

    #     return data


# TODO: NotificationSerializer exclude = ['user'] and use depth = 1
# TODO: HyperlinkedModelSerializer?
