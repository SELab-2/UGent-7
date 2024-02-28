from rest_framework import serializers
from ..models.teacher import Teacher


class TeacherSerializer(serializers.ModelSerializer):

    courses = serializers.HyperlinkedIdentityField(
        view_name='teacher-courses',
        read_only=True,
    )

    class Meta:
        model = Teacher
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculty', 'last_enrolled', 'create_time', 'courses'
          ]
