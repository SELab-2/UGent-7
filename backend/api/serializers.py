from rest_framework import serializers
from .models.teacher import Teacher
from .models.admin import Admin
from .models.assistant import Assistant
from .models.student import Student
from .models.project import Project
from .models.group import Group
from .models.course import Course


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time','courses']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time']


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time','courses']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time','courses']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'visible', 'archived', 'start_date', 'deadline', 'checks', 'course']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'academic_startyear','description','parent_course']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'project', 'students','score']
