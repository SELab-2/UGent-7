from django.utils.translation import gettext
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models.group import Group
from api.permissions.group_permissions import GroupPermission
from api.permissions.group_permissions import GroupStudentPermission
from api.serializers.group_serializer import GroupSerializer
from api.serializers.student_serializer import StudentSerializer
from api.serializers.group_serializer import StudentJoinGroupSerializer, StudentLeaveGroupSerializer
from api.serializers.project_serializer import SubmissionAddSerializer
from api.serializers.submission_serializer import SubmissionSerializer
from rest_framework.request import Request


class GroupViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser | GroupPermission]

    @action(detail=True, methods=["get"], permission_classes=[IsAdminUser | GroupStudentPermission])
    def students(self, request, **_):
        """Returns a list of students for the given group"""
        # This automatically fetches the group from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        group = self.get_object()
        students = group.students.all()

        # Serialize the student objects
        serializer = StudentSerializer(
            students, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, permission_classes=[IsAdminUser])
    def submissions(self, request, **_):
        """Returns a list of students for the given group"""
        # This automatically fetches the group from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        group = self.get_object()
        submissions = group.submissions.all()

        # Serialize the student objects
        serializer = SubmissionSerializer(
            submissions, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @students.mapping.post
    @students.mapping.put
    def _add_student(self, request, **_):
        """Add a student to the group"""
        group = self.get_object()

        serializer = StudentJoinGroupSerializer(
            data=request.data, context={"group": group}
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            group.students.add(
                serializer.validated_data["student_id"]
            )

        return Response({
            "message": gettext("group.success.students.add"),
        })

    @students.mapping.delete
    def _remove_student(self, request, **_):
        """Removes a student from the group"""
        group = self.get_object()

        serializer = StudentLeaveGroupSerializer(
            data=request.data, context={"group": group}
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            group.students.remove(
                serializer.validated_data["student_id"]
            )

        return Response({
            "message": gettext("group.success.students.remove"),
        })

    @submissions.mapping.post
    @submissions.mapping.put
    def _add_submission(self, request: Request, **_):
        """Add a submission to the group"""
        group: Group = self.get_object()

        # Add submission to course
        serializer = SubmissionAddSerializer(
            data=request.data, context={"group": group, "request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(group=group)

        return Response({
            "message": gettext("group.success.submissions.add")
        })
