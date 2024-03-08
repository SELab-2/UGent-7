from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models.group import Group
from api.permissions.group_permissions import GroupPermission
from api.serializers.group_serializer import GroupSerializer
from api.serializers.student_serializer import StudentSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser | GroupPermission]

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        """Returns a list of students for the given group"""
        # This automatically fetches the group from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        group = self.get_object()
        students = group.students.all()

        # Serialize the student objects
        serializer = StudentSerializer(
            students, many=True, context={"request": request}
        )
        return Response(serializer.data)
