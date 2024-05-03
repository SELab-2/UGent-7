from api.logic.check_folder_structure import parse_zip_file
from nh3 import clean
from api.models.checks import FileExtension
from api.models.course import Course
from api.models.group import Group
from api.models.project import Project
from api.models.submission import Submission, StructureCheckResult, ExtraCheckResult, StateEnum
from api.serializers.checks_serializer import StructureCheckSerializer
from api.serializers.course_serializer import CourseSerializer
from api.serializers.submission_serializer import SubmissionSerializer
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.translation import gettext
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

        non_empty_groups = Group.objects.filter(project=instance, students__isnull=False).distinct().count()

        groups_submitted_ids = Submission.objects.filter(group__project=instance).values_list('group__id', flat=True)
        unique_groups = set(groups_submitted_ids)
        groups_submitted = len(unique_groups)

        #  The total amount of groups with at least one submission should never exceed the total number of non empty groups
        # (the seeder does not account for this restriction)
        if (groups_submitted > non_empty_groups):
            non_empty_groups = groups_submitted

        passed_structure_checks_submission_ids = StructureCheckResult.objects.filter(
            submission__group__project=instance,
            submission__is_valid=True,
            result=StateEnum.SUCCESS
        ).values_list('submission__id', flat=True)

        passed_structure_checks_group_ids = Submission.objects.filter(
            id__in=passed_structure_checks_submission_ids
        ).values_list('group_id', flat=True)

        unique_groups = set(passed_structure_checks_group_ids)
        structure_checks_passed = len(unique_groups)

        passed_extra_checks_submission_ids = ExtraCheckResult.objects.filter(
            submission__group__project=instance,
            submission__is_valid=True,
            result=StateEnum.SUCCESS
        ).values_list('submission__id', flat=True)

        passed_extra_checks_group_ids = Submission.objects.filter(
            id__in=passed_extra_checks_submission_ids
        ).values_list('group_id', flat=True)

        unique_groups = set(passed_extra_checks_group_ids)
        extra_checks_passed = len(unique_groups)

        # The total number of passed extra checks combined with the number of passed structure checks
        # can never exceed the total number of submissions (the seeder does not account for this restriction)
        if (structure_checks_passed + extra_checks_passed > groups_submitted):
            extra_checks_passed = groups_submitted - structure_checks_passed

        return {
            "non_empty_groups": non_empty_groups,
            "groups_submitted": groups_submitted,
            "structure_checks_passed": structure_checks_passed,
            "extra_checks_passed": extra_checks_passed
        }

    class Meta:
        fields = [
            "non_empty_groups",
            "groups_submitted",
            "structure_checks_passed",
            "extra_checks_passed"
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

        data['description'] = clean(data['description'])

        return data

    class Meta:
        model = Project
        fields = "__all__"


class CreateProjectSerializer(ProjectSerializer):
    number_groups = serializers.IntegerField(min_value=0, required=False)
    zip_structure = serializers.FileField(required=False, read_only=True)

    def create(self, validated_data):
        # Pop the 'number_groups' field from validated_data
        number_groups = validated_data.pop('number_groups', None)

        # Get the zip structure file from the request
        request = self.context.get('request')
        zip_structure = request.FILES.get('zip_structure')

        # Create the project object without passing 'number_groups' field
        project = super().create(validated_data)

        if project.group_size == 1:
            # If the group_size is set to one, create a group for each student
            students = project.course.students.all()

            for student in students:
                group = Group.objects.create(project=project)
                group.students.add(student)

        elif number_groups is not None:
            # Create groups for the project, if specified

            if number_groups > 0:
                # Create the number of groups specified
                for _ in range(number_groups):
                    Group.objects.create(project=project)

            else:
                # If the number of groups is set to zero, create #students / group_size groups
                number_students = project.course.students.count()
                group_size = project.group_size

                for _ in range(0, number_students, group_size):
                    group = Group.objects.create(project=project)

        # If a zip_structure is provided, parse it to create the structure checks
        if zip_structure is not None:
            # Define the temporary storage location
            temp_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
            # Save the file to the temporary location
            temp_file_path = temp_storage.save(f"tmp/{zip_structure.name}", zip_structure)
            # Pass the full path to the parse_zip_file function
            parse_zip_file(project, temp_file_path)
            # Delete the temporary file
            temp_storage.delete(temp_file_path)

        return project


class TeacherCreateGroupSerializer(serializers.Serializer):
    number_groups = serializers.IntegerField(min_value=1)


class SubmissionStatusSerializer(serializers.Serializer):
    non_empty_groups = serializers.IntegerField(read_only=True)
    groups_submitted = serializers.IntegerField(read_only=True)
    structure_checks_passed = serializers.IntegerField(read_only=True)
    extra_checks_passed = serializers.IntegerField(read_only=True)


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


class StructureCheckAddSerializer(StructureCheckSerializer):
    def validate(self, data):
        project: Project = self.context["project"]
        if project.structure_checks.filter(name=data["name"]).count():
            raise ValidationError(gettext("project.error.structure_checks.already_existing"))

        obl_ext = set()
        for ext in self.context["obligated"]:
            extension, _ = FileExtension.objects.get_or_create(
                extension=ext
            )
            obl_ext.add(extension)
        data["obligated_extensions"] = obl_ext

        block_ext = set()
        for ext in self.context["blocked"]:
            extension, _ = FileExtension.objects.get_or_create(
                extension=ext
            )
            if extension in obl_ext:
                raise ValidationError(gettext("project.error.structure_checks.extension_blocked_and_obligated"))
            block_ext.add(extension)
        data["blocked_extensions"] = block_ext

        return data
