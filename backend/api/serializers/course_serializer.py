from rest_framework import serializers
from ..models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    assistants = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='assistant-detail'
    )

    teachers = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='teacher-detail'
    )

    students = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='student-detail'
    )

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'academic_startyear', 'description',
            'parent_course', 'teachers', 'assistants', 'students'
          ]
