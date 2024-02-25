from cas_client import CASClient
from ypovoli import settings

client = CASClient(
    server_url=settings.CAS_ENDPOINT,
    service_url=settings.API_VALIDATE_ENDPOINT,
    auth_prefix=''
)
