from rest_framework import serializers
from .models.teacher import Teacher
from .models.admin import Admin
from .models.assistant import Assistant
from .models.student import Student
from .models.project import Project
from .models.group import Group
from .models.course import Course
from .models.submission import Submission, SubmissionFile
from .models.checks import Checks, FileExtension


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='course-detail'
  )
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time','courses']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time']


class AssistantSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='course-detail'
  )
    class Meta:
        model = Assistant
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time','courses']

class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
      many=True,
      read_only=True,
      view_name='course-detail'
  )
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'faculty','last_enrolled','create_time','courses']


class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.HyperlinkedRelatedField(
      many=False,
      read_only=True,
      view_name='course-detail'
  )
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'visible', 'archived', 'start_date', 'deadline', 'checks', 'course']

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
        fields = ['id', 'name', 'academic_startyear','description','parent_course', 'teachers', 'assistants', 'students']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'project', 'students','score']

class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ['id', 'submission', 'file']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'group', 'submission_number','submission_time']

class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields = ['id', 'dockerfile']

class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = ['id', 'extension', 'allowed_file_extensions', 'forbidden_file_extensions']
