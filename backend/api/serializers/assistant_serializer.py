from rest_framework import serializers
from ..models.assistant import Assistant


class AssistantSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        view_name='assistant-courses',
        lookup_field='id',
        lookup_url_kwarg='assistant_id'
    )

    class Meta:
        model = Assistant
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculty', 'last_enrolled', 'create_time', 'courses'
          ]
