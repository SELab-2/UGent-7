from django.core.serializers import serialize
import json
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import patch
from authentication.models import User
from authentication.serializers import UserSerializer
from ypovoli import settings

USER_DATA = {
    'id': '1234',
    'username': 'ddickwd',
    'email': 'dummy@dummy.com',
    'first_name': 'dummy',
    'last_name': 'McDickwad',
}


class TestWhomAmIView(APITestCase):
    def setUp(self):
        """Create a user and generate a token for that user"""
        self.user = User.objects.create(**USER_DATA)
        access_token = AccessToken().for_user(self.user)
        self.token = f'Bearer {access_token}'

    def test_who_am_i_view_get_returns_user_if_existing_and_authenticated(self):
        """
        WhoAmIView should return the User info when requested if User
        exists in database and token is supplied.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('auth.whoami'))
        self.assertJSONEqual(response.content.decode('utf-8'), UserSerializer(self.user).data)

    def test_who_am_i_view_get_does_not_return_viewer_if_deleted_but_authenticated(self):
        """
        WhoAmIView should return that the user was not found if
        authenticated user was deleted from the database.
        """
        self.user.delete()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('auth.whoami'))
        self.assertJSONNotEqual(response.content, UserSerializer(self.user).data)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['detail'], 'User not found')

    def test_who_am_i_view_returns_401_when_not_authenticated(self):
        """WhoAmIView should return a 401 status code when the user is not authenticated"""
        response = self.client.get(reverse('auth.whoami'))
        self.assertEqual(response.status_code, 401)


class TestLogoutView(APITestCase):
    def test_logout_view_authenticated_logout_url(self):
        """LogoutView should return a logout url redirect if authenticated user sends a post request."""
        self.user = User.objects.create(**USER_DATA)
        access_token = AccessToken().for_user(self.user)
        self.token = f'Bearer {access_token}'
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse('auth.logout'))
        self.assertEqual(response.status_code, 302)
        url = '{server_url}/logout?service={service_url}'.format(
            server_url=settings.CAS_ENDPOINT,
            service_url=settings.API_ENDPOINT
        )
        self.assertEqual(response['Location'], url)

    def test_logout_view_not_authenticated_logout_url(self):
        """LogoutView should return a 401 error when trying to access it while not authenticated."""
        response = self.client.post(reverse('auth.logout'))
        self.assertEqual(response.status_code, 401)

class TestLoginView(APITestCase):
    def test_login_view_returns_login_url(self):
        """LoginView should return a login url redirect if a post request is sent."""
        response = self.client.get(reverse('auth.login'))
        self.assertEqual(response.status_code, 302)
        url = '{server_url}/login?service={service_url}'.format(
            server_url=settings.CAS_ENDPOINT,
            service_url=settings.CAS_RESPONSE
        )
        self.assertEqual(response['Location'], url)

class TestTokenEchoView(APITestCase):
    def test_token_echo_echoes_token(self):
        """TokenEchoView should echo the User's current token"""
        ticket = 'This is a ticket.'
        response = self.client.get(reverse('auth.echo'), data={'ticket': ticket})
        content = response.rendered_content.decode('utf-8').strip('"')
        self.assertEqual(content, ticket)


