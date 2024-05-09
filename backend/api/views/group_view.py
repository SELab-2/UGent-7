from api.models.group import Group
from api.permissions.group_permissions import (GroupPermission,
                                               GroupStudentPermission,
                                               GroupSubmissionPermission)
from api.serializers.group_serializer import (GroupSerializer,
                                              StudentJoinGroupSerializer,
                                              StudentLeaveGroupSerializer)
from api.serializers.student_serializer import StudentSerializer
from api.serializers.submission_serializer import SubmissionSerializer
from django.utils.translation import gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin, ListModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class GroupViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser | GroupPermission]

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | GroupStudentPermission])
    def students(self, request, **_):
        """Returns a list of students for the given group"""
        group = self.get_object()
        students = group.students.all()

        # Serialize the student objects
        serializer = StudentSerializer(
            students, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # TODO: I can access this endpoint unauthorized
    @action(detail=True, permission_classes=[IsAdminUser | GroupSubmissionPermission])
    def submissions(self, request, **_):
        """Returns a list of submissions for the given group"""
        group = self.get_object()
        submissions = group.submissions.all()

        # Serialize the student objects
        serializer = SubmissionSerializer(
            submissions, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @students.mapping.post
    @students.mapping.put
    @swagger_auto_schema(request_body=StudentJoinGroupSerializer)
    def _add_student(self, request, **_):
        """Add a student to the group"""
        group = self.get_object()

        serializer = StudentJoinGroupSerializer(
            data=request.data, context={"group": group}
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            group.students.add(
                serializer.validated_data["student"]
            )

        return Response({
            "message": gettext("group.success.students.add"),
        })

    @students.mapping.delete
    @swagger_auto_schema(request_body=StudentLeaveGroupSerializer)
    def _remove_student(self, request, **_):
        """Removes a student from the group"""
        group = self.get_object()

        serializer = StudentLeaveGroupSerializer(
            data=request.data, context={"group": group}
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            group.students.remove(
                serializer.validated_data["student"]
            )

        return Response({
            "message": gettext("group.success.students.remove"),
        })

    @submissions.mapping.post
    @submissions.mapping.put
    @swagger_auto_schema(request_body=SubmissionSerializer)
    def _add_submission(self, request: Request, **_):
        """Add a submission to the group"""
        group: Group = self.get_object()

        # Add submission to course
        serializer = SubmissionSerializer(
            data=request.data, context={"group": group, "request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(group=group)

        return Response({
            "message": gettext("group.success.submissions.add"),
            "submission": serializer.data
        })
