from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.models.group import Group
from api.models.student import Student
from api.serializers.student_serializer import StudentIDSerializer


class GroupSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="project-detail"
    )

    students = serializers.HyperlinkedIdentityField(
        view_name="group-students",
        read_only=True,
    )

    class Meta:
        model = Group
        fields = ["id", "project", "students", "score"]

    def validate(self, data):
        # Make sure the score of the group is lower or equal to the maximum score
        group: Group = self.instance

        if "score" in data and data["score"] > group.project.max_score:
            raise ValidationError(gettext("group.errors.score_exceeds_max"))

        return data


class StudentJoinGroupSerializer(StudentIDSerializer):

    def validate(self, data):
        # The validator needs the group context.
        if "group" not in self.context:
            raise ValidationError(gettext("group.error.context"))

        # Get the group and student
        group: Group = self.context["group"]
        student: Student = data["student_id"]

        # Make sure the group is not already full
        if group.is_full():
            raise ValidationError(gettext("group.errors.full"))

        # Make sure the student is part of the course
        if not group.project.course.students.filter(id=student.id).exists():
            raise ValidationError(gettext("group.errors.not_in_course"))

        # Make sure the student is not already in a group
        if student.is_enrolled_in_group(group.project):
            raise ValidationError(gettext("group.errors.already_in_group"))

        return data


class StudentLeaveGroupSerializer(StudentIDSerializer):

    def validate(self, data):
        # The validator needs the group context.
        if "group" not in self.context:
            raise ValidationError(gettext("group.error.context"))

        # Get the group and student
        group: Group = self.context["group"]
        student: Student = data["student_id"]

        # Make sure the student was in the group
        if not group.students.filter(id=student.id).exists():
            raise ValidationError(gettext("group.errors.not_present"))

        return data
