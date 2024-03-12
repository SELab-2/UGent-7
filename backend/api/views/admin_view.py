from rest_framework import viewsets
from authentication.serializers import UserSerializer
from authentication.models import User


class AdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer
