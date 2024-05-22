from api.models.assistant import Assistant
from api.models.teacher import Teacher
from django.http import HttpResponseRedirect

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
from rest_framework.status import HTTP_200_OK
from ypovoli import settings


class CASViewSet(ViewSet):
    # The IsAuthenticated class is applied by default,
    # but it's good to be verbose when it comes to security.
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def login(self, request: Request) -> HttpResponseRedirect:
        """Attempt to log in. Redirect to our single CAS endpoint."""
        should_echo = request.query_params.get('echo', False)

        if should_echo == "1":
            client._service_url = settings.CAS_DEBUG_RESPONSE

        return redirect(client.get_login_url())

    @action(detail=False, methods=['POST'])
    def logout(self, request) -> Response:
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


def create_user(self, request, data) -> tuple[User, bool]:
    """General function to create a user, log them in and which returns an empty html page"""
    # log in user, or retrieve if they already exist
    user, created = User.objects.get_or_create(id=data["id"], defaults=data)

    # if it has just been created, send the signal to user_created Signal(), to also activate it as a student
    if created:
        user_created.send(sender=self, attributes={**data, "ugentStudentID": data.id}, user=user)

    # login the user
    login(request, user)

    # return Response with empty html page
    return user, created


response = Response('<!DOCTYPE html><html></html>',
                    status=HTTP_200_OK, headers={"Location": "/"}, content_type="text/html")


class TestUser(ViewSet):
    """View meant to be able to log in quickly for tests on server in debug mode"""

    permission_classes = [IsDebug]

    @action(detail=False, methods=['POST'], permission_classes=[IsDebug], url_path='student')
    def login_student(self, request, *__) -> Response:
        """This endpoint lets you log in as a student who's not an admin"""
        create_user(self, request, settings.TEST_STUDENT_DATA)
        return response

    @action(detail=False, methods=['POST'], permission_classes=[IsDebug], url_path='professor')
    def login_professor(self, request, *__) -> Response:
        """This endpoint lets you log in as a professor"""
        user, created = create_user(self, request, settings.TEST_PROFESSOR_DATA)
        if created:
            Teacher.create(user)

    @action(detail=False, methods=['POST'], permission_classes=[IsDebug], url_path='multi')
    def login_multi(self, request, *__) -> Response:
        """This endpoint lets you log in as a user who's a student, an assistant and a professor at the same time"""
        user, created = create_user(self, request, settings.TEST_MULTI_DATA)
        if created:
            Assistant.create(user)
            Teacher.create(user)
        return response

    @action(detail=False, methods=['POST'], permission_classes=[IsDebug], url_path='admin')
    def login_admin(self, request, *__) -> Response:
        """This endpoint lets you log in an admin"""
        create_user(self, request, settings.TEST_ADMIN_DATA)
        return response
