from nh3 import clean
from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.serializers.student_serializer import StudentIDSerializer
from api.serializers.teacher_serializer import TeacherIDSerializer
from api.serializers.faculty_serializer import FacultySerializer
from api.models.course import Course
from authentication.models import Faculty


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.HyperlinkedIdentityField(
        view_name="course-teachers",
        read_only=True,
    )

    assistants = serializers.HyperlinkedIdentityField(
        view_name="course-assistants",
        read_only=True,
    )

    students = serializers.HyperlinkedIdentityField(
        view_name="course-students",
        read_only=True,
    )

    projects = serializers.HyperlinkedIdentityField(
        view_name="course-projects",
        read_only=True,
    )

    parent_course = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="course-detail"
    )

    faculty = FacultySerializer(
        read_only=True
    )

    def validate(self, attrs: dict) -> dict:
        """Extra custom validation for course serializer"""
        attrs['description'] = clean(attrs['description'])
        return attrs

    class Meta:
        model = Course
        fields = "__all__"


class CreateCourseSerializer(CourseSerializer):
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        required=False,
        allow_null=True,
    )

    def create(self, validated_data):
        faculty = validated_data.pop('faculty', None)

        # Create the course
        course = super().create(validated_data)

        # Link the faculty, if specified
        if faculty is not None:
            course.faculty = faculty
            course.save()

        return course

    
    def update(self, instance, validated_data):
        faculty = validated_data.pop('faculty', None)

        # Update the course
        course = super().update(instance, validated_data)

        # Link the faculty, if specified
        if faculty is not None:
            course.faculty = faculty
            course.save()

        return course


class CourseIDSerializer(serializers.Serializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )


class CourseCloneSerializer(serializers.Serializer):
    clone_teachers = serializers.BooleanField()
    clone_assistants = serializers.BooleanField()


class StudentJoinSerializer(StudentIDSerializer):
    def validate(self, data):
        # The validator needs the course context.
        if "course" not in self.context:
            raise ValidationError(gettext("courses.error.context"))

        course: Course = self.context["course"]

        # Check if the student isn't already enrolled.
        if course.students.contains(data["student"]):
            raise ValidationError(gettext("courses.error.students.already_present"))

        # Check if the course is not from a past academic year.
        if course.is_past():
            raise ValidationError(gettext("courses.error.past_course"))

        return data


class StudentLeaveSerializer(StudentIDSerializer):
    def validate(self, data):
        # The validator needs the course context.
        if "course" not in self.context:
            raise ValidationError(gettext("courses.error.context"))

        course: Course = self.context["course"]

        # Make sure the student is enrolled.
        if not course.students.contains(data["student"]):
            raise ValidationError(gettext("courses.error.students.not_present"))

        # Check if the course is not from a past academic year.
        if course.is_past():
            raise ValidationError(gettext("courses.error.past_course"))

        return data


class TeacherJoinSerializer(TeacherIDSerializer):
    def validate(self, data):
        # The validator needs the course context.
        if "course" not in self.context:
            raise ValidationError(gettext("courses.error.context"))

        course: Course = self.context["course"]

        # Check if the teacher isn't already enrolled.
        if course.teachers.contains(data["teacher"]):
            raise ValidationError(gettext("courses.error.teachers.already_present"))

        # Check if the course is not from a past academic year.
        if course.is_past():
            raise ValidationError(gettext("courses.error.past_course"))

        return data


class TeacherLeaveSerializer(TeacherIDSerializer):
    def validate(self, data):
        # The validator needs the course context.
        if "course" not in self.context:
            raise ValidationError(gettext("courses.error.context"))

        course: Course = self.context["course"]

        # Make sure the teacher is enrolled.
        if not course.teachers.contains(data["teacher"]):
            raise ValidationError(gettext("courses.error.teachers.not_present"))

        # Check if the course is not from a past academic year.
        if course.is_past():
            raise ValidationError(gettext("courses.error.past_course"))

        return data
