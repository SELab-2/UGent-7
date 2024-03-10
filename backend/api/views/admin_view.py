from django.utils.translation import gettext
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from authentication.serializers import UserSerializer, UserIDSerializer
from authentication.models import User


class AdminViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        # Add an Admin
        serializer = UserIDSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(serializer.validated_data["user_id"])
            user.make_admin()

        return Response({
            "message": gettext("admins.success.add")
        })