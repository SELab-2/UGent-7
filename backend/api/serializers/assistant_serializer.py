from rest_framework import serializers
from ..models.assistant import Assistant


class AssistantSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='course-detail'
    )

    class Meta:
        model = Assistant
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculty', 'last_enrolled', 'create_time', 'courses'
          ]
