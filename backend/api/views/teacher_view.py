from django.utils.translation import gettext
from django.db.models.functions import Concat
from rest_framework.pagination import PageNumberPagination
from django.db.models import Value
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from api.models.teacher import Teacher
from api.serializers.teacher_serializer import TeacherSerializer, TeacherIDSerializer
from api.serializers.course_serializer import CourseSerializer
from api.permissions.teacher_permissions import TeacherPermission
from authentication.serializers import UserIDSerializer
from api.views.pagination.user_pagination import UserPagination


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser | TeacherPermission]

    @swagger_auto_schema(request_body=UserIDSerializer)
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Add the student role to the user"""
        serializer = UserIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            Teacher.create(serializer.validated_data.get('user'))

        return Response({
            "message": gettext("teachers.success.add")
        })

    @action(detail=False, pagination_class=UserPagination)
    def search(self, request: Request) -> Response:
        # Extract filter params
        search = request.query_params.get("search", "")
        roles = request.query_params.getlist("roles[]")
        faculties = request.query_params.getlist("faculties[]")

        # Make sure that if roles are passed, teacher is a selected role
        if roles and "teacher" not in roles:
            queryset = []

        else:
            # Filter the queryset based on the search term
            queryset = Teacher.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                full_name__icontains=search
            )

            # Filter the queryset based on selected faculties
            if faculties:
                queryset = queryset.filter(faculties__id__in=faculties)

        # Serialize the resulting queryset
        serializer = self.serializer_class(self.paginate_queryset(queryset), many=True, context={
            "request": request
        })

        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=TeacherIDSerializer)
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Delete the student role from the user"""
        self.get_object().deactivate()

        return Response({
            "message": gettext("teachers.success.destroy")
        })

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
