from rest_framework import serializers
from ..models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    assistants = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='assistant-detail'
    )

    teachers = serializers.HyperlinkedIdentityField(
      view_name='course-teachers',  # View that handles the hyperlink
      lookup_field='id',            # Field to use for the lookup
      lookup_url_kwarg='course_id'  # URL keyword argument to use
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
