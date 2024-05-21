from api.models.group import Group
from api.models.student import Student
from api.permissions.role_permissions import (is_assistant, is_student,
                                              is_teacher)
from api.serializers.project_serializer import ProjectSerializer
from api.serializers.student_serializer import StudentIDSerializer
from django.utils.translation import gettext
from notifications.signals import NotificationType, notification_create
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class GroupSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(
        read_only=True,
    )

    students = serializers.HyperlinkedIdentityField(
        view_name="group-students",
        read_only=True,
    )

    submissions = serializers.HyperlinkedIdentityField(
        view_name="group-submissions",
        read_only=True,
    )

    class Meta:
        model = Group
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = self.context["request"].user
        course_id = instance.project.course.id

        # If you are not a student, you can always see the score
        if is_student(user):
            student_in_course = user.student.courses.filter(id=course_id).exists()
            # Student can not see the score if they are not part of the course associated with group and
            # neither an assistant or a teacher,
            # or it is not visible yet when they are part of the course associated with the group
            if not student_in_course and not is_assistant(user) and not is_teacher(user) or \
                    not instance.project.score_visible and student_in_course:
                data.pop("score")

        return data

    def validate(self, attrs):
        # Make sure the score of the group is lower or equal to the maximum score
        self.instance: Group
        group = self.instance

        if "score" in attrs and attrs["score"] > group.project.max_score:
            raise ValidationError(gettext("group.errors.score_exceeds_max"))

        return attrs


class StudentJoinGroupSerializer(StudentIDSerializer):

    def validate(self, attrs):
        # The validator needs the group context.
        if "group" not in self.context:
            raise ValidationError(gettext("group.error.context"))

        # Get the group and student
        group: Group = self.context["group"]
        student: Student = attrs["student"]

        # Make sure a student can't join if groups are locked
        if group.project.is_groups_locked():
            raise ValidationError(gettext("group.errors.locked"))

        # Make sure the group is not already full
        if group.is_full():
            raise ValidationError(gettext("group.errors.full"))

        # Make sure the student is part of the course
        if not group.project.course.students.filter(id=student.id).exists():
            raise ValidationError(gettext("group.errors.not_in_course"))

        # Make sure the student is not already in a group
        if student.is_enrolled_in_group(group.project):
            raise ValidationError(gettext("group.errors.already_in_group"))

        return attrs


class StudentLeaveGroupSerializer(StudentIDSerializer):

    def validate(self, attrs):
        # The validator needs the group context.
        if "group" not in self.context:
            raise ValidationError(gettext("group.error.context"))

        # Get the group and student
        group: Group = self.context["group"]
        student: Student = attrs["student"]

        # Make sure the student was in the group
        if not group.students.filter(id=student.id).exists():
            raise ValidationError(gettext("group.errors.not_present"))

        # Make sure a student can't leave if groups are locked
        if group.project.is_groups_locked():
            raise ValidationError(gettext("group.errors.locked"))

        return attrs
