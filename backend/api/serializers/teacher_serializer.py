from rest_framework import serializers
from ..models.teacher import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        view_name="teacher-courses",
        read_only=True,
    )

    faculties = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="faculty-detail"
    )

    class Meta:
        model = Teacher
        fields = "__all__"
