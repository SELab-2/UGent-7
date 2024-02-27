from rest_framework import serializers
from ..models.teacher import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
      view_name='teacher-courses',
      lookup_field='id',
      lookup_url_kwarg='teacher_id'
    )

    class Meta:
        model = Teacher
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculty', 'last_enrolled', 'create_time', 'courses'
          ]
