import cas_client
from django.test import TestCase
from unittest.mock import patch

from ..serializers import CASTokenObtainSerializer, UserSerializer


def service_validate(
        self,
        ticket=None,
        service_url=None,
        headers=None,):
    response = {}
    if ticket != "1":
        response.error = "This is an error"
    else:
        response.data = {
            "ugentID": 1234,
            "uid": 4321,
            "mail": "dummy@dummy.be",
            "givenname": "Dummy",
            "surname": "McDickwad",
            "faculty": "Sciences",
            "lastenrolled": ""
        }


class SerializersTests(TestCase):
    @patch.object(cas_client.CASClient, 'perform_service_validate', service_validate)
    def test_invalid_ticket_generates_error(self):
        pass