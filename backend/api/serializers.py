from rest_framework import serializers
from .models.teacher import Teacher
from .models.admin import Admin
from .models.assistant import Assistant


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
