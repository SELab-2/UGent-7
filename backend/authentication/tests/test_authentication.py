from cas_client import CASClient
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
from authentication.serializers import CASTokenObtainSerializer, UserSerializer


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
        user = UserSerializer(data={
            'id': ID,
            'username': USERNAME,
            'email': 'dummy',
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        })
        user2 = UserSerializer(data={
            'id': ID,
            'username': USERNAME,
            'email': "dummy@dummy",
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        })
        user3 = UserSerializer(data={
            'id': ID,
            'username': USERNAME,
            'email': 21,
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        })
        self.assertFalse(user.is_valid())
        self.assertFalse(user2.is_valid())
        self.assertFalse(user3.is_valid())

    def test_valid_id_and_username_and_email_makes_valid_serializer(self):
        user = UserSerializer(data={
            'id': ID,
            'username': USERNAME,
            'email': EMAIL,
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
        })
        self.assertTrue(user.is_valid())


def customize_data(ugent_id, uid, mail):

    class Response:
        __slots__ = ('error', 'data')

        def __init__(self):
            self.error = None
            self.data = {}

    def service_validate(
            self,
            ticket=None,
            service_url=None,
            headers=None,):
        response = Response()
        if ticket != TICKET:
            response.error = "This is an error"
        else:
            response.data['attributes'] = {
                'ugentID': ugent_id,
                'uid': uid,
                'mail': mail,
                'givenname': FIRST_NAME,
                'surname': LAST_NAME,
                'faculty': "Sciences",
                'lastenrolled': "2023 - 2024",
                'lastlogin': "",
                'createtime': ""
            }
        return response

    return service_validate


class SerializersTests(TestCase):
    @patch.object(CASClient,
                  'perform_service_validate',
                  customize_data(ID, USERNAME, EMAIL))
    def test_invalid_ticket_generates_error(self):
        """When the wrong ticket is provided, a ValidationError should be raised."""
        # I have set "1" as the correct ticket hereµ
        serializer = CASTokenObtainSerializer(data={
            'token': RefreshToken(),
            'ticket': WRONG_TICKET
        })
        self.assertFalse(serializer.is_valid())
