from authentication.models import User
from authentication.serializers import UserIDSerializer, UserSerializer
from django.utils.translation import gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class AdminViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=UserIDSerializer)
    def create(self, request: Request) -> Response:
        """
        Make the provided user admin by setting `is_staff` = true.
        """
        serializer = UserIDSerializer(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data["user"].make_admin()

        return Response({
            "message": gettext("admins.success.add")
        })
