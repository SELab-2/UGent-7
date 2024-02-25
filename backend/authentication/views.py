from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.serializers import CASTicketSerializer, UserSerializer
from authentication.services import users
from authentication.cas.client import client
from ypovoli import settings

@api_view(['GET'])
def whoami(_: Request) -> Response:
    pass

@api_view(['GET'])
def login(_: Request) -> Response:
    """Attempt to log in.
    Redirect to our single CAS endpoint.
    """
    return redirect(
        client.get_login_url()
    )

@api_view(['GET'])
def validate(request: Request) -> Response:
    """Validate a Service Ticket obtained from the CAS endpoint.
    Returns a user token for further API authentication.
    """
    ticket = CASTicketSerializer(data=request.query_params)

    if ticket.is_valid():
        user = UserSerializer(
            users.get_or_create(**ticket.validated_data['user'])
        )

        return Response(user.data)

    return Response({
        'errors': ticket.errors
    })

@api_view(['POST'])
def logout(request: Request) -> Response:
    """Attempt to log out.
    Redirect to our single CAS endpoint.
    """
    return redirect(
        client.get_logout_url(
            service_url=settings.API_ENDPOINT
        )
    )
