from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _
from api.views.check_folder_structure import get_zip_structure, check_zip_structure, parseZipFile
from ..models.project import Project
from ..serializers.project_serializer import ProjectSerializer
from ..serializers.group_serializer import GroupSerializer
from ..serializers.checks_serializer import StructureCheckSerializer, ExtraCheckSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["get"])
    def groups(self, request, pk=None):
        """Returns a list of groups for the given project"""

        try:
            queryset = Project.objects.get(id=pk)
            groups = queryset.groups.all()

            # Serialize the group objects
            serializer = GroupSerializer(
                groups, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Project.DoesNotExist:
            # Invalid project ID
            raise NotFound(_('project.status.not_found'))

    @action(detail=True, methods=["get"])
    def structure_checks(self, request, pk=None):
        """Returns the structure checks for the given project"""

        try:
            queryset = Project.objects.get(id=pk)
            checks = queryset.structure_checks.all()

            # Serialize the check objects
            serializer = StructureCheckSerializer(
                checks, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Project.DoesNotExist:
            # Invalid project ID
            raise NotFound(_('project.status.not_found'))

    @action(detail=True, methods=["get"])
    def extra_checks(self, request, pk=None):
        """Returns the extra checks for the given project"""

        try:
            queryset = Project.objects.get(id=pk)
            checks = queryset.extra_checks.all()

            # Serialize the check objects
            serializer = ExtraCheckSerializer(
                checks, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Project.DoesNotExist:
            # Invalid project ID
            raise NotFound(_('project.status.not_found'))
