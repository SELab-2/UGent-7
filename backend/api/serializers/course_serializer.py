from rest_framework import serializers
from ..models.course import Course


class CourseSerializer(serializers.ModelSerializer):

    teachers = serializers.HyperlinkedIdentityField(
        view_name='course-teachers',
        read_only=True,
    )

    assistants = serializers.HyperlinkedIdentityField(
        view_name='course-assistants',
        read_only=True,
    )

    students = serializers.HyperlinkedIdentityField(
        view_name='course-students',
        read_only=True,
    )

    projects = serializers.HyperlinkedIdentityField(
        view_name='course-projects',
        read_only=True,
    )

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'academic_startyear', 'description',
            'parent_course', 'teachers', 'assistants', 'students', 'projects'
          ]
