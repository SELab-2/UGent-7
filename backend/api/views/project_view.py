from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.views.check_folder_structure import get_zip_structure, check_zip_structure, data_directory, parseZipFile
from ..models.project import Project
from ..serializers.project_serializer import ProjectSerializer
from ..serializers.group_serializer import GroupSerializer


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
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "Project not found"}
            )
