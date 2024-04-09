from django.utils.translation import gettext
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from api.permissions.assistant_permissions import AssistantPermission
from api.models.assistant import Assistant
from api.serializers.assistant_serializer import AssistantSerializer, AssistantIDSerializer
from api.serializers.course_serializer import CourseSerializer
from authentication.serializers import UserIDSerializer


class AssistantViewSet(ModelViewSet):

    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsAdminUser | AssistantPermission]

    @swagger_auto_schema(request_body=UserIDSerializer)
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Add the student role to the user"""
        serializer = UserIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            Assistant.create(serializer.validated_data.get('user'))

        return Response({
            "message": gettext("teachers.success.add")
        })

    @swagger_auto_schema(request_body=AssistantIDSerializer)
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Delete the student role from the user"""
        self.get_object().deactivate()

        return Response({
            "message": gettext("teachers.success.destroy")
        })

    @action(detail=True, methods=["get"])
    def courses(self, request, **_):
        """Returns a list of courses for the given assistant"""
        assistant = self.get_object()
        courses = assistant.courses

        # Serialize the course objects
        serializer = CourseSerializer(
            courses, many=True, context={"request": request}
        )

        return Response(serializer.data)
