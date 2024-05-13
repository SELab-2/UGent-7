import json

from api.tests.helpers import create_admin, create_faculty
from authentication.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class AdminModelTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(  # type: ignore
            User.get_dummy_admin()
        )

    def test_no_admins(self):
        """
        able to retrieve no admin before publishing it.
        """

        response_root = self.client.get(reverse("admin-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")  # type: ignore
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_admin_exists(self):
        """
        Able to retrieve a single admin after creating it.
        """
        admin = create_admin(
            id=3, first_name="John", last_name="Doe", email="john.doe@example.com"
        )

        # Make a GET request to retrieve the admin
        response = self.client.get(reverse("admin-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one admin
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved admin match the created admin
        retrieved_admin = content_json[0]
        self.assertEqual(int(retrieved_admin["id"]), admin.id)
        self.assertEqual(retrieved_admin["first_name"], admin.first_name)
        self.assertEqual(retrieved_admin["last_name"], admin.last_name)
        self.assertEqual(retrieved_admin["email"], admin.email)

    def test_multiple_admins(self):
        """
        Able to retrieve multiple admins after creating them.
        """
        # Create multiple admins
        admin1 = create_admin(
            id=1, first_name="Saul", last_name="Goodman", email="john.doe@example.com"
        )

        admin2 = create_admin(
            id=2, first_name="Liv", last_name="Doe", email="jane.doe@example.com"
        )

        # Make a GET request to retrieve the admins
        response = self.client.get(reverse("admin-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple admins
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved admins match the created admins
        retrieved_admin1, retrieved_admin2 = content_json
        self.assertEqual(int(retrieved_admin1["id"]), admin1.id)
        self.assertEqual(retrieved_admin1["first_name"], admin1.first_name)
        self.assertEqual(retrieved_admin1["last_name"], admin1.last_name)
        self.assertEqual(retrieved_admin1["email"], admin1.email)

        self.assertEqual(int(retrieved_admin2["id"]), admin2.id)
        self.assertEqual(retrieved_admin2["first_name"], admin2.first_name)
        self.assertEqual(retrieved_admin2["last_name"], admin2.last_name)
        self.assertEqual(retrieved_admin2["email"], admin2.email)

    def test_admin_detail_view(self):
        """
        Able to retrieve details of a single admin.
        """
        # Create an admin for testing with the name "Bob Peeters"
        admin = create_admin(
            id=5, first_name="Bob", last_name="Peeters", email="bob.peeters@example.com"
        )

        # Make a GET request to retrieve the admin details
        response = self.client.get(
            reverse("admin-detail", args=[str(admin.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved admin match the created admin
        self.assertEqual(int(content_json["id"]), admin.id)
        self.assertEqual(content_json["first_name"], admin.first_name)
        self.assertEqual(content_json["last_name"], admin.last_name)
        self.assertEqual(content_json["email"], admin.email)

    def test_admin_faculty(self):
        """
        Able to retrieve faculty details of a single admin.
        """
        # Create an admin for testing with the name "Bob Peeters"
        faculty = create_faculty(name="testing faculty")
        admin = create_admin(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com",
            faculty=[faculty],
        )

        # Make a GET request to retrieve the admin details
        response = self.client.get(
            reverse("admin-detail", args=[str(admin.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved admin match the created admin
        self.assertEqual(int(content_json["id"]), admin.id)
        self.assertEqual(content_json["first_name"], admin.first_name)
        self.assertEqual(content_json["last_name"], admin.last_name)
        self.assertEqual(content_json["email"], admin.email)

        response = self.client.get(content_json["faculties"][0], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content_json["name"], faculty.name)
