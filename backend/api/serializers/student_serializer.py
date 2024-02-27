from rest_framework import serializers
from ..models.student import Student


class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
      view_name='student-courses',
      lookup_field='id',
      lookup_url_kwarg='student_id'
    )

    groups = serializers.HyperlinkedIdentityField(
      view_name='student-groups',
      lookup_field='id',
      lookup_url_kwarg='student_id'
    )

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'email', 'faculty',
            'last_enrolled', 'create_time', 'courses', 'groups'
          ]
