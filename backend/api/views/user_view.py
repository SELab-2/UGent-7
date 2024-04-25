from django.db.models.functions import Concat
from django.db.models import Value
from api.permissions.notification_permissions import NotificationPermission
from api.permissions.role_permissions import IsSameUser
from api.views.pagination.basic_pagination import BasicPagination
from authentication.models import User
from authentication.serializers import UserSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsSameUser]

    @action(detail=True, methods=['PATCH'], url_path='admin', permission_classes=[IsAdminUser])
    def patch_admin(self, request: Request, **_) -> Response:
        """
        Update the user's admin status with is_staff in request query parameters
        """
        # request.data needs to contain user id in 'user' field
        if request.data.get("is_staff"):
            self.get_object().make_admin()
        else:
            self.get_object().remove_admin()

        return Response(status=HTTP_200_OK)

    @action(detail=False)
    def search(self, request: Request) -> Response:
        self.pagination_class = BasicPagination

        search = request.query_params.get("search", "")
        identifier = request.query_params.get("id", "")
        username = request.query_params.get("username", "")
        email = request.query_params.get("email", "")
        roles = request.query_params.getlist("roles[]")

        # Search parameters for a simple name + faculty filter
        name = request.query_params.get("name", None)
        faculties = request.query_params.getlist("faculties[]")

        # If name is provided, just filter by the name (and faculties if provided)
        if name or faculties:
            queryset = self.get_queryset().annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                full_name__icontains=name
            )

            # Filter the queryset based on selected faculties
            if faculties:
                queryset = queryset.filter(faculties__id__in=faculties)

            serializer = self.serializer_class(self.paginate_queryset(queryset), many=True, context={
                "request": request
            })

            return self.get_paginated_response(serializer.data)

        # Otherwise, search by the provided search term
        queryset1 = self.get_queryset().filter(
            id__icontains=search
        )
        queryset2 = self.get_queryset().filter(
            username__icontains=search
        )
        queryset3 = self.get_queryset().filter(
            email__icontains=search
        )
        queryset4 = self.get_queryset().all()
        if "student" in roles:
            queryset4 = queryset4.intersection(
                self.get_queryset().filter(student__isnull=False, student__is_active=True)
            )
        if "assistant" in roles:
            queryset4 = queryset4.intersection(
                self.get_queryset().filter(assistant__isnull=False, assistant__is_active=True)
            )
        if "teacher" in roles:
            queryset4 = queryset4.intersection(
                self.get_queryset().filter(teacher__isnull=False, teacher__is_active=True)
            )
        queryset1 = queryset1.union(queryset2, queryset3)
        queryset = self.get_queryset().filter(
            id__icontains=identifier,
            username__icontains=username,
            email__icontains=email
        )
        queryset = queryset.intersection(queryset1, queryset4)

        serializer = self.serializer_class(self.paginate_queryset(queryset), many=True, context={
            "request": request
        })

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[NotificationPermission])
    def notifications(self, request: Request, pk: str):
        """Returns a list of notifications for the given user"""
        notifications = Notification.objects.filter(user=pk)
        serializer = NotificationSerializer(
            notifications, many=True, context={"request": request}
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[NotificationPermission],
        url_path="notifications/read",
    )
    def read(self, request: Request, pk: str):
        """Marks all notifications as read for the given user"""
        notifications = Notification.objects.filter(user=pk)
        notifications.update(is_read=True)

        return Response(status=HTTP_200_OK)
