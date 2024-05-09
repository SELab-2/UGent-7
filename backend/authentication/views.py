from authentication.cas.client import client
from authentication.permissions import IsDebug
from authentication.serializers import CASTokenObtainSerializer, UserSerializer
from authentication.models import User
from authentication.signals import user_created
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_301_MOVED_PERMANENTLY
from ypovoli import settings


class CASViewSet(ViewSet):
    # The IsAuthenticated class is applied by default,
    # but it's good to be verbose when it comes to security.
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def login(self, request: Request) -> Response:
        """Attempt to log in. Redirect to our single CAS endpoint."""
        should_echo = request.query_params.get('echo', False)

        if should_echo == "1" and settings.DEBUG:
            client._service_url = settings.CAS_DEBUG_RESPONSE

        return redirect(client.get_login_url())

    @action(detail=False, methods=['POST'])
    def logout(self, request: Request) -> Response:
        """Log out the current user."""
        logout(request)

        return Response()

    @action(detail=False, methods=['GET'], url_path='whoami', url_name='whoami')
    def who_am_i(self, request: Request) -> Response:
        """Get the user account data for the logged-in user.
        The logged-in user is determined by the provided access token in the
        Authorization HTTP header.
        """
        user_serializer = UserSerializer(request.user, context={
            'request': request
        })

        return Response(
            user_serializer.data
        )

    @action(detail=False, methods=['GET'], permission_classes=[IsDebug])
    def echo(self, request: Request) -> Response:
        """Echo the obtained CAS token for development and testing."""
        token_serializer = CASTokenObtainSerializer(data=request.query_params, context={
            'request': request
        })

        if token_serializer.is_valid():
            return Response(token_serializer.validated_data)

        raise AuthenticationFailed(token_serializer.errors)


data = {
    "id": "1234",
    "username": "test",
    "email": "test@test",
    "first_name": "test",
    "last_name": "test",
}

attributes = dict(data)
attributes["ugentStudentID"] = "1234"


def create_user(self, request) -> Response:
    user, created = User.objects.get_or_create(id=data["id"], defaults=data)

    if created:
        user_created.send(sender=self, attributes=attributes, user=user)

    login(request, user)

    return Response(status=HTTP_301_MOVED_PERMANENTLY, headers={"Location": "/"})


class TestUser(ViewSet):
    permission_classes = [IsDebug]

    @action(detail=False, methods=['GET'], permission_classes=[IsDebug], url_path='admin')
    def login_admin(self, request, *__) -> Response:
        data["is_staff"] = True
        return create_user(self, request)

    @action(detail=False, methods=['GET'], permission_classes=[IsDebug], url_path='student')
    def login_student(self, request, *__) -> Response:
        data["is_staff"] = False
        return create_user(self, request)
