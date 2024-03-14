from rest_framework import serializers
from api.models.student import Student


class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        view_name="student-courses",
        read_only=True,
    )

    groups = serializers.HyperlinkedIdentityField(
        view_name="student-groups",
        read_only=True,
    )

    faculties = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="faculty-detail"
    )

    class Meta:
        model = Student
        fields = '__all__'


class StudentIDSerializer(serializers.Serializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    )
