import json

from django.test import TestCase
from django.urls import reverse

from ..models.checks import FileExtension


def create_fileExtension(id, extension):
    """
    Create a FileExtension with the given arguments.
    """
    return FileExtension.objects.create(
        id=id,
        extension=extension
    )

"""
def create_checks(id, allowed_file_extensions, forbidden_file_extensions):

    # Create a Checks with the given arguments.

    return Checks.objects.create(
        id=id,
        allowed_file_extensions=allowed_file_extensions,
        forbidden_file_extensions=forbidden_file_extensions
    )
"""


class FileExtensionModelTests(TestCase):
    def test_no_fileExtension(self):
        """
        able to retrieve no FileExtension before publishing it.
        """

        response_root = self.client.get(reverse("fileExtension-list"), follow=True)
        # print(response.content)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_fileExtension_exists(self):
        """
        Able to retrieve a single fileExtension after creating it.
        """
        fileExtension = create_fileExtension(
            id=5,
            extension=".pdf"
        )

        # Make a GET request to retrieve the fileExtension
        response = self.client.get(reverse("fileExtension-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one admin
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved admin match the created admin
        retrieved_fileExtension = content_json[0]
        self.assertEqual(
            int(retrieved_fileExtension["id"]), fileExtension.id)
        self.assertEqual(
            retrieved_fileExtension["extension"], fileExtension.extension)

    def test_multiple_fileExtension(self):
        """
        Able to retrieve multiple fileExtension after creating them.
        """
        # Create multiple fileExtension
        fileExtension1 = create_fileExtension(
            id=1,
            extension=".jpg"
            )
        fileExtension2 = create_fileExtension(
            id=2,
            extension=".png"
            )

        # Make a GET request to retrieve the fileExtension
        response = self.client.get(reverse("fileExtension-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple admins
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved admins match the created admins
        retrieved_fileExtension1, retrieved_fileExtension2 = content_json
        self.assertEqual(
            int(retrieved_fileExtension1["id"]), fileExtension1.id)
        self.assertEqual(
            retrieved_fileExtension1["extension"], fileExtension1.extension)

        self.assertEqual(
            int(retrieved_fileExtension2["id"]), fileExtension2.id)
        self.assertEqual(
            retrieved_fileExtension2["extension"], fileExtension2.extension)

    def test_fileExtension_detail_view(self):
        """
        Able to retrieve details of a single fileExtension.
        """
        # Create an fileExtension for testing with the name "Bob Peeters"
        fileExtension = create_fileExtension(
            id=3,
            extension=".zip"
            )

        # Make a GET request to retrieve the fileExtension details
        response = self.client.get(
            reverse(
                "fileExtension-detail",
                args=[str(fileExtension.id)]),
            follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved fileExtension
        # match the created fileExtension
        self.assertEqual(int(content_json["id"]), fileExtension.id)
        self.assertEqual(content_json["extension"], fileExtension.extension)
