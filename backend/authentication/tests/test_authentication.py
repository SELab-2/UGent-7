import cas_client
from django.test import TestCase
from rest_framework.serializers import ValidationError
from unittest.mock import patch

from ..serializers import CASTokenObtainSerializer, UserSerializer


def customize_data(ugent_id, uid, mail):

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
                "ugentID": ugent_id,
                "uid": uid,
                "mail": mail,
                "givenname": "Dummy",
                "surname": "McDickwad",
                "faculty": "Sciences",
                "lastenrolled": "2021-05-21",
                "lastlogin": "",
                "createtime": ""
            }
        return response

    return service_validate


class UserSerializerModelTests(TestCase):
    def test_non_string_id_makes_user_serializer_invalid(self):
        """
        The is_valid() method of a UserSerializer whose supplied User's ID is not a string
        should return False.
        """
        user = UserSerializer(data={
            "id": 1234
        })
        self.assertFalse(user.is_valid())

    def test_non_string_username_makes_user_serializer_invalid(self):
        """
        The is_valid() method of a UserSerializer whose supplied User's username is not a string
        should return False.
        """
        user = UserSerializer(data={
            "username": 10
        })
        self.assertFalse(user.is_valid())

    def test_invalid_email_makes_user_serializer_invalid(self):
        """
        The is_valid() method of a UserSerializer whose supplied User's email is not
        formatted as an email address should return False.
        """
        user = UserSerializer(data={
            "email": "dummy"
        })
        user2 = UserSerializer(data={
            "email": "dummy@dummy"
        })
        user3 = UserSerializer(data={
            "email": 21
        })
        self.assertFalse(user.is_valid())
        self.assertFalse(user2.is_valid())
        self.assertFalse(user3.is_valid())


class SerializersTests(TestCase):
    class CASTokenObtain:
        def __init__(self, ticket):
            self.token = "ABCD"
            self.ticket = ticket

    @patch.object(cas_client.CASClient,
                  'perform_service_validate',
                  customize_data("1234", "ddickwd", "dummy@dummy.be"))
    def test_invalid_ticket_generates_error(self):
        """When the wrong ticket is provided, a ValidationError should be raised."""
        # I have set "1" as the correct ticket here
        obtain = self.CASTokenObtain("2")
        serializer = CASTokenObtainSerializer(obtain)
        self.assertRaises(ValidationError, lambda: serializer.validate(serializer.ticket))
