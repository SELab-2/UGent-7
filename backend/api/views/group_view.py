from django.utils.translation import gettext
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models.group import Group
from api.permissions.group_permissions import GroupPermission
from api.permissions.group_permissions import GroupStudentPermission
from api.permissions.role_permissions import IsStudent
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
    
    @action(detail=True, methods=["post"], permission_classes=[GroupStudentPermission])
    def join(self, request, pk=None):
        """Enrolls the authenticated student in the group"""
        group = self.get_object()
        student = request.user.student

        # Make sure the group is not full
        if group.is_full():
            raise ValidationError(gettext("group.errors.full"))
        
        # Make sure the student is not already in a group
        if student.is_enrolled_in_group(group.project):
            raise ValidationError(gettext("group.errors.already_in_group"))
        
        # Add the student to the group
        group.students.add(student)

        return Response({
            "message": gettext("group.success.joined"),
        })

