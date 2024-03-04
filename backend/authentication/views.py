from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from authentication.cas.client import client
from ypovoli import settings

class CASViewSet(ViewSet):

    @action(detail=False, methods=['get'])
    def login(self, _: Request) -> Response:
        """Attempt to log in. Redirect to our single CAS endpoint."""
        return redirect(client.get_login_url())

    @action(detail=False, methods=['get'])
    def logout(self, _: Request) -> Response:
        """Attempt to log out. Redirect to our single CAS endpoint.
        Normally would only allow POST requests to a logout endpoint.
        Since the CAS logout location handles the actual logout, we should accept GET requests.
        """
        return redirect(client.get_logout_url(service_url=settings.API_ENDPOINT))

    @action(detail=False, methods=['get'], url_path='whoami')
    def who_am_i(self, request: Request) -> Response:
        """Get the user account data for the logged-in user.
        The logged-in user is determined by the provided access token in the
        Authorization HTTP header.
        """
        return Response(
            UserSerializer(request.user).data
        )

    @action(detail=False, methods=['get'])
    def echo(self, request: Request) -> Response:
        """Echo the obtained CAS token for development and testing."""
        return Response(request.query_params.get('ticket'))