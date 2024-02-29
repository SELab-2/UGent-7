import datetime
import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models.admin import Admin


def create_admin(id, first_name, last_name, username, email):
    """
    Create a Admin with the given arguments.
    """
    return Admin.objects.create(
            id=id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            create_time=timezone.now(),
        )


class AdminModelTests(TestCase):
    def test_no_admins(self):
        """
        able to retrieve no admin before publishing it.
        """

        # print(reverse("api:admin.index"))
        response_root = self.client.get("https://localhost:8080/admins")
        # print(response.content)
        self.assertEqual(response_root.status_code, 301)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])
