from rest_framework import serializers
from ..models.teacher import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='course-detail'
    )

    class Meta:
        model = Teacher
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculty', 'last_enrolled', 'create_time', 'courses'
          ]
