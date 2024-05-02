from api.models.group import Group
from api.models.project import Project
from api.models.submission import Submission, StructureCheckResult, ExtraCheckResult, StateEnum
from api.permissions.project_permissions import (ProjectGroupPermission,
                                                 ProjectPermission)
from api.serializers.checks_serializer import (ExtraCheckSerializer,
                                               StructureCheckSerializer)
from api.serializers.group_serializer import GroupSerializer
from api.serializers.project_serializer import (ProjectSerializer,
                                                StructureCheckAddSerializer,
                                                SubmissionStatusSerializer,
                                                TeacherCreateGroupSerializer)
from api.serializers.submission_serializer import SubmissionSerializer
from django.utils.translation import gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


# TODO: Error message when creating a project with wrongly formatted date looks a bit weird
class ProjectViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser | ProjectPermission]  # GroupPermission has exact the same logic as for a project

    @action(detail=True, permission_classes=[IsAdminUser | ProjectGroupPermission])
    def groups(self, request, **_):
        """Returns a list of groups for the given project"""
        # This automatically fetches the group from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        project = self.get_object()
        groups = project.groups.all()

        # Serialize the group objects
        serializer = GroupSerializer(
            groups, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True)
    def submissions(self, request, **_):
        """Returns a list of submissions for the given project"""
        project = self.get_object()
        submissions = Submission.objects.filter(group__project=project)

        # Serialize the group objects
        serializer = SubmissionSerializer(
            submissions, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @groups.mapping.post
    @groups.mapping.put
    @swagger_auto_schema(request_body=TeacherCreateGroupSerializer)
    def _create_groups(self, request, **_):
        """Create a number of groups for the project"""
        project = self.get_object()

        serializer = TeacherCreateGroupSerializer(
            data=request.data, context={"project": project}
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            # Get the number of groups to create
            num_groups = serializer.validated_data["number_groups"]

            # Create the groups
            for _ in range(num_groups):
                Group.objects.create(
                    project=project
                )

        return Response({
            "message": gettext("project.success.groups.created"),
        })

    @action(detail=True, methods=["get"])
    def structure_checks(self, request, **_):
        """Returns the structure checks for the given project"""
        project = self.get_object()
        checks = project.structure_checks.all()

        # Serialize the check objects
        serializer = StructureCheckSerializer(
            checks, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @structure_checks.mapping.post
    @structure_checks.mapping.put
    @swagger_auto_schema(request_body=StructureCheckAddSerializer)
    def _add_structure_check(self, request: Request, **_):
        """Add a structure_check to the project"""

        project: Project = self.get_object()

        # TODO: Crashes when requesting without any fields, shouldn't be given as context. Validator needs to check it
        serializer = StructureCheckAddSerializer(
            data=request.data,
            context={
                "project": project,
                "request": request,
                "obligated": request.data.getlist('obligated_extensions'),
                "blocked": request.data.getlist('blocked_extensions')
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project)

        return Response({
            "message": gettext("project.success.structure_check.add")
        })

    @action(detail=True, methods=["get"])
    def extra_checks(self, request, **_):
        """Returns the extra checks for the given project"""
        project = self.get_object()
        checks = project.extra_checks.all()

        # Serialize the check objects
        serializer = ExtraCheckSerializer(
            checks, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @extra_checks.mapping.post
    @swagger_auto_schema(request_body=ExtraCheckSerializer)
    def _add_extra_check(self, request: Request, **_):
        """Add an extra_check to the project"""

        project: Project = self.get_object()

        serializer = ExtraCheckSerializer(
            data=request.data,
            context={
                "project": project,
                "request": request
            }
        )

        # TODO: Weird error message when invalid docker_image id
        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project)

        return Response({
            "message": gettext("project.success.extra_check.add")
        })

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | ProjectGroupPermission])
    def submission_status(self, request, **_):
        """Returns the current submission status for the given project
        This includes:
            - The total amount of groups that contain at least one student
            - The amount of groups that have uploaded a submission
            - The amount of submissions that passed the basic tests
        """
        project = self.get_object()

        non_empty_groups = Group.objects.filter(project=project, students__isnull=False).distinct().count()

        groups_submitted_ids = Submission.objects.filter(group__project=project).values_list('group__id', flat=True)
        unique_groups = set(groups_submitted_ids)
        groups_submitted = len(unique_groups)

        #  The total amount of groups with at least one submission should never exceed the total number of non empty groups
        # (the seeder does not account for this restriction)
        if (groups_submitted > non_empty_groups):
            non_empty_groups = groups_submitted

        passed_structure_checks_submission_ids = StructureCheckResult.objects.filter(
            submission__group__project=project,
            submission__is_valid=True,
            result=StateEnum.SUCCESS
        ).values_list('submission__id', flat=True)

        passed_structure_checks_group_ids = Submission.objects.filter(
            id__in=passed_structure_checks_submission_ids
        ).values_list('group_id', flat=True)

        unique_groups = set(passed_structure_checks_group_ids)
        structure_checks_passed = len(unique_groups)

        passed_extra_checks_submission_ids = ExtraCheckResult.objects.filter(
            submission__group__project=project,
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

        serializer = SubmissionStatusSerializer({
            "non_empty_groups": non_empty_groups,
            "groups_submitted": groups_submitted,
            "structure_checks_passed": structure_checks_passed,
            "extra_checks_passed": extra_checks_passed
        })

        return Response(serializer.data)
