from api.logic.check_folder_structure import parse_zip_file
from api.models.group import Group
from api.models.project import Project
from api.models.submission import Submission
from api.serializers.checks_serializer import StructureCheckSerializer
from api.serializers.course_serializer import CourseSerializer
from api.serializers.submission_serializer import SubmissionSerializer
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.translation import gettext
from nh3 import clean
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SubmissionStatusSerializer(serializers.Serializer):
    non_empty_groups = serializers.IntegerField(read_only=True)
    groups_submitted = serializers.IntegerField(read_only=True)
    submissions_passed = serializers.IntegerField(read_only=True)

    def to_representation(self, instance: Project):
        """Return the submission status of the project"""
        if not isinstance(instance, Project):
            raise ValidationError(gettext("project.errors.invalid_instance"))

        non_empty_groups = instance.groups.filter(students__isnull=False).count()
        groups_submitted = Submission.objects.filter(group__project=instance).count()
        submissions_passed = Submission.objects.filter(group__project=instance, is_valid=True).count()

        return {
            "non_empty_groups": non_empty_groups,
            "groups_submitted": groups_submitted,
            "submissions_passed": submissions_passed,
        }

    class Meta:
        fields = [
            "non_empty_groups",
            "groups_submitted",
            "submissions_passed",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    # We want the course to be eager loaded
    course = CourseSerializer(
        read_only=True
    )

    # We want the status to be eager loaded
    status = SubmissionStatusSerializer(
        source="*",
        read_only=True
    )

    structure_checks = serializers.HyperlinkedIdentityField(
        view_name="project-structure-checks",
        read_only=True
    )

    extra_checks = serializers.HyperlinkedIdentityField(
        view_name="project-extra-checks",
        read_only=True
    )

    groups = serializers.HyperlinkedIdentityField(
        view_name="project-groups",
        read_only=True
    )

    submissions = serializers.HyperlinkedIdentityField(
        view_name="project-submissions",
        read_only=True
    )

    def validate(self, data):
        """Validate the serializer data"""
        if not self.partial:
            # Only require course if it is not a partial update
            if "course" in self.context:
                data["course_id"] = self.context["course"].id
            else:
                raise ValidationError(gettext("project.errors.context"))

        # Check if start date of the project is not in the past
        if "start_date" in data and data["start_date"] < timezone.now().replace(hour=0, minute=0, second=0):
            raise ValidationError(gettext("project.errors.start_date_in_past"))

        # Set the start date depending on if it is a partial update and whether it was given by the user
        if "start_date" not in data:
            if self.partial:
                start_date = self.instance.start_date
            else:
                start_date = timezone.now()
        else:
            start_date = data["start_date"]

        # Check if deadline of the project is before the start date
        if "deadline" in data and data["deadline"] < start_date:
            raise ValidationError(gettext("project.errors.deadline_before_start_date"))

        if "description" in data:
            data['description'] = clean(data['description'])

        return data

    def create(self, validated_data):
        # Pop the 'number_groups' field from validated_data
        number_groups = validated_data.pop('number_groups', None)

        # Get the zip structure file from the request
        # TODO: ?
        request = self.context.get('request')
        zip_structure = request.FILES.get('zip_structure')

        # Create the project object without passing 'number_groups' field
        project = super().create(validated_data)

        # Create groups for the project, if specified
        if number_groups is not None:

            for _ in range(number_groups):
                Group.objects.create(project=project)

        elif project.group_size == 1:
            # If the group_size is set to one, create a group for each student
            students = project.course.students.all()

            for student in students:
                group = Group.objects.create(project=project)
                group.students.add(student)

        # If a zip_structure is provided, parse it to create the structure checks
        # TODO: Move to background celery
        if zip_structure is not None:
            # Define the temporary storage location
            temp_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
            # Save the file to the temporary location
            temp_file_path = temp_storage.save(f"tmp/{zip_structure.name}", zip_structure)
            # Pass the full path to the parse_zip_file function
            result = parse_zip_file(project, temp_file_path)
            # Delete the temporary file
            temp_storage.delete(temp_file_path)
            if not result:
                raise ValidationError(gettext("project.errors.zip_structure"))

        return project

    class Meta:
        model = Project
        fields = "__all__"


class CreateProjectSerializer(ProjectSerializer):
    # Only require these fields when creating a project
    number_groups = serializers.IntegerField(min_value=1, required=False)
    zip_structure = serializers.FileField(required=False, read_only=True)


class TeacherCreateGroupSerializer(serializers.Serializer):
    number_groups = serializers.IntegerField(min_value=1)


class SubmissionAddSerializer(SubmissionSerializer):
    def validate(self, data):

        group: Group = self.context["group"]
        project: Project = group.project

        # Check if the project's deadline is not passed.
        if project.deadline_passed():
            raise ValidationError(gettext("project.error.submissions.past_project"))

        if not project.is_visible():
            raise ValidationError(gettext("project.error.submissions.non_visible_project"))

        if project.is_archived():
            raise ValidationError(gettext("project.error.submissions.archived_project"))

        return data
