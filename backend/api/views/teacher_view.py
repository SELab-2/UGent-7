from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from api.models.teacher import Teacher
from api.serializers.teacher_serializer import TeacherSerializer
from api.serializers.course_serializer import CourseSerializer
from api.permissions.teacher_permissions import TeacherPermission
from rest_framework.permissions import IsAuthenticated


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser | TeacherPermission]

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def courses(self, request, pk=None):
        """Returns a list of courses for the given teacher"""
        teacher = self.get_object()
        courses = teacher.courses.all()

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )

        return Response(serializer.data)
