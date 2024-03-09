from django.utils.translation import gettext
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions.project_permissions import ProjectGroupPermission, ProjectPermission
from api.models.group import Group
from ..models.project import Project
from ..serializers.project_serializer import ProjectSerializer
from ..serializers.group_serializer import GroupSerializer
from ..serializers.checks_serializer import StructureCheckSerializer, ExtraCheckSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser | ProjectPermission]  # GroupPermission has exact the same logic as for a project

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | ProjectGroupPermission])
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

    @groups.mapping.post
    def _create_groups(self, request, **_):
        """Create a number of groups for the project"""
        project = self.get_object()

        # Get the number of groups to create
        num_groups = int(request.data.get("number_groups", 0))

        # Create the groups
        for _ in range(max(0, num_groups)):
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
