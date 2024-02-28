from rest_framework import serializers
from ..models.course import Course


class CourseSerializer(serializers.ModelSerializer):

    teachers = serializers.HyperlinkedIdentityField(
        view_name='course-teachers', 
        read_only=True,
    )

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'academic_startyear', 'description',
            'parent_course', 'teachers', 'assistants', 'students', 'projects'
          ]
