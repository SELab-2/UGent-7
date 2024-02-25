from rest_framework import viewsets
from ..models.assistant import Assistant
from ..serializers import AssistantSerializer


class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer