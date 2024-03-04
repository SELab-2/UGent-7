from django.test import TestCase

from unittest.mock import patch, Mock

from rest_framework_simplejwt.tokens import RefreshToken

from authentication.cas.client import client
from authentication.serializers import CASTokenObtainSerializer, UserSerializer
from authentication.signals import user_created, user_login


TICKET = "ST-da8e1747f248a54a5f078e3905b88a9767f11d7aedcas6"
WRONG_TICKET = "ST-da8e1747f248a54a5f078e3905b88a9767f11d7aedcas5"

ID = "1234"
USERNAME = "ddickwd"
EMAIL = "dummy@dummy.be"
FIRST_NAME = "Dummy"
LAST_NAME = "McDickwad"


class UserSerializerModelTests(TestCase):
    def test_invalid_email_makes_user_serializer_invalid(self):
        """
        The is_valid() method of a UserSerializer whose supplied User's email is not
        formatted as an email address should return False.
        """
        user = UserSerializer(
            data={
                "id": ID,
                "username": USERNAME,
                "email": "dummy",
                "first_name": FIRST_NAME,
                "last_name": LAST_NAME,
            }
        )
        user2 = UserSerializer(
            data={
                "id": ID,
                "username": USERNAME,
                "email": "dummy@dummy",
                "first_name": FIRST_NAME,
                "last_name": LAST_NAME,
            }
        )
        user3 = UserSerializer(
            data={
                "id": ID,
                "username": USERNAME,
                "email": 21,
                "first_name": FIRST_NAME,
                "last_name": LAST_NAME,
            }
        )
        self.assertFalse(user.is_valid())
        self.assertFalse(user2.is_valid())
        self.assertFalse(user3.is_valid())

    def test_valid_email_makes_valid_serializer(self):
        """
        When the serializer is provided with a valid email, the serializer becomes valid,
        thus the is_valid() method returns True.
        """
        user = UserSerializer(
            data={
                "id": ID,
                "username": USERNAME,
                "email": EMAIL,
                "first_name": FIRST_NAME,
                "last_name": LAST_NAME,
            }
        )
        self.assertTrue(user.is_valid())


def customize_data(ugent_id, uid, mail):
    class Response:
        __slots__ = ("error", "data")

        def __init__(self):
            self.error = None
            self.data = {}

    def service_validate(
        ticket=None,
        service_url=None,
        headers=None,
    ):
        response = Response()
        if ticket != TICKET:
            response.error = "This is an error"
        else:
            response.data["attributes"] = {
                "ugentID": ugent_id,
                "uid": uid,
                "mail": mail,
                "givenname": FIRST_NAME,
                "surname": LAST_NAME,
                "faculty": "Sciences",
                "lastenrolled": "2023 - 2024",
                "lastlogin": "",
                "createtime": "",
            }
        return response

    return service_validate


class SerializersTests(TestCase):
    def test_wrong_length_ticket_generates_error(self):
        """
        When the provided ticket has the wrong length, a ValidationError should be raised
        when validating the serializer.
        """
        serializer = CASTokenObtainSerializer(
            data={"token": RefreshToken(), "ticket": "ST"}
        )
        self.assertFalse(serializer.is_valid())

    @patch.object(
        client, "perform_service_validate", customize_data(ID, USERNAME, EMAIL)
    )
    def test_wrong_ticket_generates_error(self):
        """
        When the wrong ticket is provided, a ValidationError should be raised when trying to validate
        the serializer.
        """
        serializer = CASTokenObtainSerializer(
            data={"token": RefreshToken(), "ticket": WRONG_TICKET}
        )
        self.assertFalse(serializer.is_valid())

    @patch.object(
        client, "perform_service_validate", customize_data(ID, USERNAME, "dummy@dummy")
    )
    def test_wrong_user_arguments_generate_error(self):
        """
        If the user arguments returned by CAS are not valid, then a ValidationError
        should be raised when validating the serializer.
        """
        serializer = CASTokenObtainSerializer(
            data={"token": RefreshToken(), "ticket": TICKET}
        )
        self.assertFalse(serializer.is_valid())

    @patch.object(
        client, "perform_service_validate", customize_data(ID, USERNAME, EMAIL)
    )
    def test_new_user_activates_user_created_signal(self):
        """
        If the authenticated user is new to the app, then the user_created signal should
        be sent when trying to validate the token."""

        mock = Mock()
        user_created.connect(mock, dispatch_uid="STDsAllAround")
        serializer = CASTokenObtainSerializer(
            data={"token": RefreshToken(), "ticket": TICKET}
        )
        # this next line triggers the retrieval of User information and logs in the user
        serializer.is_valid()
        self.assertEquals(mock.call_count, 1)

    @patch.object(
        client, "perform_service_validate", customize_data(ID, USERNAME, EMAIL)
    )
    def test_old_user_does_not_activate_user_created_signal(self):
        """
        If the authenticated user is new to the app, then the user_created signal should
        be sent when trying to validate the token."""

        mock = Mock()
        user_created.connect(mock, dispatch_uid="STDsAllAround")
        serializer = CASTokenObtainSerializer(
            data={"token": RefreshToken(), "ticket": TICKET}
        )
        # this next line triggers the retrieval of User information and logs in the user
        serializer.is_valid()
        self.assertEquals(mock.call_count, 0)

    @patch.object(
        client, "perform_service_validate", customize_data(ID, USERNAME, EMAIL)
    )
    def test_login_signal(self):
        """
        When the token is correct and all user data is correct, while trying to validate
        the token, then the user_login signal should be sent.
        """
        mock = Mock()
        user_login.connect(mock, dispatch_uid="STDsAllAround")
        serializer = CASTokenObtainSerializer(
            data={"token": RefreshToken(), "ticket": TICKET}
        )
        # this next line triggers the retrieval of User information and logs in the user
        serializer.is_valid()
        self.assertEquals(mock.call_count, 1)
