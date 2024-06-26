from api.models.group import Group
from api.models.project import Project
from api.models.student import Student
from api.models.submission import Submission
from api.permissions.project_permissions import (ProjectGroupPermission,
                                                 ProjectPermission)
from api.permissions.role_permissions import is_student, IsStudent
from api.serializers.checks_serializer import (ExtraCheckSerializer,
                                               StructureCheckSerializer)
from api.serializers.group_serializer import GroupSerializer
from api.serializers.project_serializer import (ProjectSerializer,
                                                SubmissionStatusSerializer,
                                                TeacherCreateGroupSerializer)
from api.serializers.submission_serializer import SubmissionSerializer
from django.utils.translation import gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import (DestroyModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


# TODO: Error message when creating a project with wrongly formatted date looks a bit weird
class ProjectViewSet(RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser | ProjectPermission]  # GroupPermission has exact the same logic as for a project

    @action(detail=True, permission_classes=[IsAdminUser | ProjectGroupPermission], url_path='student-group')
    def student_group(self, request: Request, **_) -> Response:
        """Returns the group of the student for the given project"""

        # Get the student object from the user
        student = Student.objects.get(id=request.user.id)

        # Get the group of the student for the project
        group = student.groups.filter(project=self.get_object()).first()

        if group is None:
            return Response(None)

        # Serialize the group object
        serializer = GroupSerializer(
            group, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True, permission_classes=[IsAdminUser | ProjectGroupPermission])
    def groups(self, request, **_):
        """Returns a list of groups for the given project"""
        # This automatically fetches the group from the URL.
        # It automatically gives back a 404 HTTP response in case of not found.
        project = self.get_object()
        groups = project.groups.all()

        # Serialize the group objects
        serializer = GroupSerializer(
            groups, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True)
    def submissions(self, request, **_):
        """Returns a list of submissions for the given project"""
        project = self.get_object()
        submissions = Submission.objects.filter(group__project=project)

        # Serialize the group objects
        serializer = SubmissionSerializer(
            submissions, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @groups.mapping.post
    @groups.mapping.put
    @swagger_auto_schema(request_body=TeacherCreateGroupSerializer)
    def _create_groups(self, request, **_):
        """Create a number of groups for the project"""
        project = self.get_object()

        serializer = TeacherCreateGroupSerializer(
            data=request.data, context={"project": project}
        )

        # Validate the serializer
        if serializer.is_valid(raise_exception=True):
            # Get the number of groups to create
            num_groups = serializer.validated_data["number_groups"]

            # Create the groups
            for _ in range(num_groups):
                Group.objects.create(
                    project=project
                )

        return Response({
            "message": gettext("project.success.groups.created"),
        })

    @action(detail=True, methods=['get'])
    def structure_checks(self, request, **_):
        """Returns the structure checks for the given project"""
        project = self.get_object()
        checks = project.structure_checks.all()

        # Serialize the check objects
        serializer = StructureCheckSerializer(
            checks,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

    @structure_checks.mapping.post
    @swagger_auto_schema(request_body=StructureCheckSerializer)
    def _add_structure_check(self, request: Request, **_):
        """Add a structure_check to the project"""
        project: Project = self.get_object()

        serializer = StructureCheckSerializer(
            data=request.data,
            context={
                "project": project,
                "request": request
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project)

        return Response(serializer.data)

    @structure_checks.mapping.put
    @swagger_auto_schema(request_body=StructureCheckSerializer)
    def _set_structure_checks(self, request: Request, **_) -> Response:
        """Set the structure checks of the given project"""
        project: Project = self.get_object()

        # Delete all current structure checks of the project
        project.structure_checks.all().delete()

        # Create the new structure checks
        serializer = StructureCheckSerializer(
            data=request.data,
            many=True,
            context={
                'project': project,
                'request': request
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project)

        return Response(serializer.validated_data)

    @action(detail=True)
    def extra_checks(self, request, **_):
        """Returns the extra checks for the given project"""
        project = self.get_object()
        checks = project.extra_checks.all()

        # Serialize the check objects
        serializer = ExtraCheckSerializer(
            checks, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @extra_checks.mapping.post
    @swagger_auto_schema(request_body=ExtraCheckSerializer)
    def _add_extra_check(self, request: Request, **_):
        """Add an extra_check to the project"""

        project: Project = self.get_object()

        serializer = ExtraCheckSerializer(
            data=request.data,
            context={
                "project": project,
                "request": request
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project)

        return Response({
            "message": gettext("project.success.extra_check.add")
        })

    @extra_checks.mapping.put
    @swagger_auto_schema(request_body=ExtraCheckSerializer)
    def set_extra_checks(self, request: Request, **_):
        """Set the extra checks of the given project"""
        project: Project = self.get_object()

        # Delete all current extra checks of the project
        project.extra_checks.all().delete()

        # Create the new extra checks
        serializer = ExtraCheckSerializer(
            data=request.data,
            many=True,
            context={
                "project": project,
                "request": request
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(project=project)

        return Response(serializer.validated_data)

    @action(detail=True, permission_classes=[IsAdminUser | ProjectGroupPermission])
    def submission_status(self, _: Request):
        """Returns the current submission status for the given project
        This includes:
            - The total amount of groups that contain at least one student
            - The amount of groups that have uploaded a submission
            - The amount of submissions that passed the basic tests
        """
        project = self.get_object()
        non_empty_groups = project.groups.filter(students__isnull=False).count()
        groups_submitted = Submission.objects.filter(group__project=project).count()
        submissions_passed = Submission.objects.filter(group__project=project, is_valid=True).count()

        serializer = SubmissionStatusSerializer({
            "non_empty_groups": non_empty_groups,
            "groups_submitted": groups_submitted,
            "submissions_passed": submissions_passed,
        })

        return Response(serializer.data)
