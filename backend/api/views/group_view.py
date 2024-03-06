from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.group import Group
from ..serializers.group_serializer import GroupSerializer
from ..serializers.student_serializer import StudentSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        """Returns a list of students for the given group"""

        try:
            queryset = Group.objects.get(id=pk)
            students = queryset.students.all()

            # Serialize the student objects
            serializer = StudentSerializer(
                students, many=True, context={"request": request}
            )
            return Response(serializer.data)

        except Group.DoesNotExist:
            # Invalid group ID
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "Group not found"}
            )
