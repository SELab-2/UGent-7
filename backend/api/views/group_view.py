from rest_framework import viewsets
from ..models.group import Group
from ..serializers.group_serializer import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
