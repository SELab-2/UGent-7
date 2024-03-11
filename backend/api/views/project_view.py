from django.utils.translation import gettext
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions.project_permissions import ProjectGroupPermission, ProjectPermission
from api.models.group import Group
from ..models.project import Project
from ..serializers.checks_serializer import StructureCheckSerializer, ExtraCheckSerializer
from api.serializers.project_serializer import ProjectSerializer, TeacherCreateGroupSerializer, SubmissionStatusSerializer
from api.serializers.group_serializer import GroupSerializer
from api.serializers.submission_serializer import SubmissionSerializer


class ProjectViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet):

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

    """
    @action(detail=True, permission_classes=[IsAdminUser])
    def submissions(self, request, **_):
        # Returns a list of subbmisions for the given project
        # This automatically fetches the group from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        project = self.get_object()
        submissions = project.submissions.all()

        # Serialize the group objects
        serializer = SubmissionSerializer(
            submissions, many=True, context={"request": request}
        )

        return Response(serializer.data)
    """

    @groups.mapping.post
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

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | ProjectGroupPermission])
    def submission_status(self, request, **_):
        """Returns the current submission status for the given project
        This includes:
            - The amount of groups that have uploaded a submission
            - The amount of submissions that passed the basic tests
            - The total amount of groups
        """
        project = self.get_object()
        groups_total = project.groups.count()
        groups_submitted = None
        submissions_passed = None

        # TODO: Once submissions is implemented, pass these arguments to the serializer as well

        serializer = SubmissionStatusSerializer({
            "groups_total": groups_total,
            # "groups_submitted": groups_submitted,
            # "submissions_passed": submissions_passed,
        })

        return Response(serializer.data)
