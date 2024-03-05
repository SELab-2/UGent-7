from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers import UserSerializer
from authentication.cas.client import client
from ypovoli import settings


class CASViewSet(ViewSet):
    # The IsAuthenticated class is applied by default,
    # but it's good to be verbose when it comes to security.
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def login(self, _: Request) -> Response:
        """Attempt to log in. Redirect to our single CAS endpoint."""
        return redirect(client.get_login_url())

    @action(detail=False, methods=['GET'])
    def logout(self, _: Request) -> Response:
        """Attempt to log out. Redirect to our single CAS endpoint.
        Normally would only allow POST requests to a logout endpoint.
        Since the CAS logout location handles the actual logout, we should accept GET requests.
        """
        return redirect(client.get_logout_url(service_url=settings.API_ENDPOINT))

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

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def echo(self, request: Request) -> Response:
        """Echo the obtained CAS token for development and testing."""
        return Response(request.query_params.get('ticket'))