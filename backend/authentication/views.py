from django.shortcuts import redirect, reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from cas_client import CASClient
from authentication.serializers import ValidateSerializer
from ypovoli import settings

client = CASClient(
    server_url=settings.CAS_ENDPOINT,
    service_url=settings.API_VALIDATE_ENDPOINT,
    auth_prefix=''
)

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
    serializer = ValidateSerializer(data=request.query_params)

    if serializer.is_valid():
        response = client.perform_service_validate(ticket=serializer.data['ticket'])

        if response.success:
            # Fetch or create user, generate token
            return Response(response.data)
        else:
            return Response({
                'errors': response.error
            })

    return Response({
        'errors': serializer.errors
    })

@api_view(['GET'])
def logout(request: Request) -> Response:
    """Attempt to log out.
    Redirect to our single CAS endpoint.
    """
    raise NotImplementedError()
