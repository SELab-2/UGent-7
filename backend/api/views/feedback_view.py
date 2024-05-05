from rest_framework import viewsets

from api.models.feedback import Feedback
from api.permissions.feedback_permissions import IsAdminOrTeacherForPatch
from api.permissions.role_permissions import is_teacher
from api.serializers.feedback_serializer import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrTeacherForPatch]