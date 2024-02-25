from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from authentication.serializers import UserSerializer
from authentication.cas.client import client
from ypovoli import settings


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Get the user account data for the current user"""
        return Response(UserSerializer(request.user).data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Attempt to log out. Redirect to our single CAS endpoint."""
        return redirect(client.get_logout_url(service_url=settings.API_ENDPOINT))

class LoginView(APIView):
    def get(self, request: Request):
        """Attempt to log in. Redirect to our single CAS endpoint."""
        return redirect(client.get_login_url())

class TokenEchoView(APIView):
    def get(self, request: Request) -> Response:
        return Response(request.query_params.get('ticket'))