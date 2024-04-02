from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from api.permissions.student_permissions import StudentPermission
from api.permissions.role_permissions import IsSameUser, IsTeacher
from api.models.student import Student
from api.serializers.student_serializer import StudentSerializer
from api.serializers.course_serializer import CourseSerializer
from api.serializers.group_serializer import GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser | StudentPermission]

    @action(detail=True)
    def courses(self, request, **_):
        """Returns a list of courses for the given student"""
        student = self.get_object()
        courses = student.courses.all()

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True)
    def groups(self, request, **_):
        """Returns a list of groups for the given student"""
        student = self.get_object()
        groups = student.groups.all()

        # Serialize the group objects
        serializer = GroupSerializer(
            groups, many=True, context={"request": request}
        )
        return Response(serializer.data)
