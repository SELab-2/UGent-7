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
from api.serializers.project_serializer import ProjectSerializer, TeacherCreateGroupSerializer
from api.serializers.project_serializer import StructureCheckAddSerializer
from api.serializers.group_serializer import GroupSerializer
from api.serializers.submission_serializer import SubmissionSerializer
from rest_framework.request import Request


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

    @structure_checks.mapping.post
    @structure_checks.mapping.put
    def _add_structure_check(self, request: Request, **_):
        """Add an structure_check to the project"""

        project: Project = self.get_object()

        # Add submission to course
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
