from api.permissions.notification_permissions import NotificationPermission
from api.permissions.role_permissions import IsSameUser, IsTeacher
from api.views.pagination.basic_pagination import BasicPagination
from authentication.models import User
from authentication.serializers import UserSerializer
from django.db.models import Q, Value
from django.db.models.functions import Concat
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet


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
        if request.data.get("is_staff"):  # type: ignore
            self.get_object().make_admin()
        else:
            self.get_object().remove_admin()

        return Response(status=HTTP_200_OK)

    @action(detail=False, pagination_class=BasicPagination, permission_classes=[IsAdminUser | IsTeacher])
    def search(self, request: Request) -> Response:
        search = request.query_params.get("search", "")
        identifier = request.query_params.get("id", "")
        username = request.query_params.get("username", "")
        email = request.query_params.get("email", "")
        name = request.query_params.get("name", "")
        roles = request.query_params.getlist("roles[]", [])
        faculties = request.query_params.getlist("faculties[]", [])

        # Setup the queryset
        queryset = self.get_queryset().annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(id__icontains=search)
            | Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(full_name__icontains=search)
        )

        # Filter the queryset based on selected roles
        role_filters = Q()

        for role in roles:
            role_filters |= Q(**{f"{role}__isnull": False, f"{role}__is_active": True})

        queryset = queryset.filter(
            role_filters,
            id__icontains=identifier,
            username__icontains=username,
            email__icontains=email,
            full_name__icontains=name
        )

        if len(faculties) > 0:
            queryset = queryset.filter(faculties__id__in=faculties)

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
    def read(self, _: Request, pk: str):
        """Marks all notifications as read for the given user"""
        notifications = Notification.objects.filter(user=pk)
        notifications.update(is_read=True)

        return Response(status=HTTP_200_OK)
