import json

from django.test import TestCase
from django.urls import reverse

from ..models.checks import FileExtension, Checks


def create_fileExtension(id, extension):
    """
    Create a FileExtension with the given arguments.
    """
    return FileExtension.objects.create(id=id, extension=extension)


def create_checks(id, allowed_file_extensions, forbidden_file_extensions):
    """Create a Checks with the given arguments."""
    check = Checks.objects.create(
        id=id,
    )

    for ext in allowed_file_extensions:
        check.allowed_file_extensions.add(ext)
    for ext in forbidden_file_extensions:
        check.forbidden_file_extensions.add(ext)
    return check


class FileExtensionModelTests(TestCase):
    def test_no_fileExtension(self):
        """
        able to retrieve no FileExtension before publishing it.
        """
        response_root = self.client.get(reverse("fileExtension-list"), follow=True)
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
        fileExtension = create_fileExtension(id=5, extension="pdf")

        # Make a GET request to retrieve the fileExtension
        response = self.client.get(reverse("fileExtension-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one fileExtension
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved fileExtension
        # match the created fileExtension
        retrieved_fileExtension = content_json[0]
        self.assertEqual(retrieved_fileExtension["extension"], fileExtension.extension)

    def test_multiple_fileExtension(self):
        """
        Able to retrieve multiple fileExtension after creating them.
        """
        # Create multiple fileExtension
        fileExtension1 = create_fileExtension(id=1, extension="jpg")
        fileExtension2 = create_fileExtension(id=2, extension="png")

        # Make a GET request to retrieve the fileExtension
        response = self.client.get(reverse("fileExtension-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple fileExtension
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved fileExtension
        # match the created fileExtension
        retrieved_fileExtension1, retrieved_fileExtension2 = content_json
        self.assertEqual(
            retrieved_fileExtension1["extension"], fileExtension1.extension
        )

        self.assertEqual(
            retrieved_fileExtension2["extension"], fileExtension2.extension
        )

    def test_fileExtension_detail_view(self):
        """
        Able to retrieve details of a single fileExtension.
        """
        # Create an fileExtension for testing.
        fileExtension = create_fileExtension(id=3, extension="zip")

        # Make a GET request to retrieve the fileExtension details
        response = self.client.get(
            reverse("fileExtension-detail", args=[str(fileExtension.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved fileExtension
        # match the created fileExtension
        self.assertEqual(content_json["extension"], fileExtension.extension)


class ChecksModelTests(TestCase):
    def test_no_checks(self):
        """
        Able to retrieve no Checks before publishing it.
        """
        response_root = self.client.get(reverse("check-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        self.assertEqual(response_root.accepted_media_type, "application/json")
        content_json = json.loads(response_root.content.decode("utf-8"))
        self.assertEqual(content_json, [])

    def test_checks_exists(self):
        """
        Able to retrieve a single Checks after creating it.
        """
        # Create a Checks instance with some file extensions
        fileExtension1 = create_fileExtension(id=1, extension="jpg")
        fileExtension2 = create_fileExtension(id=2, extension="png")
        fileExtension3 = create_fileExtension(id=3, extension="tar")
        fileExtension4 = create_fileExtension(id=4, extension="wfp")
        checks = create_checks(
            id=5,
            allowed_file_extensions=[fileExtension1, fileExtension4],
            forbidden_file_extensions=[fileExtension2, fileExtension3],
        )

        # Make a GET request to retrieve the Checks
        response = self.client.get(reverse("check-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one Checks
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved Checks match the created Checks
        retrieved_checks = content_json[0]
        self.assertEqual(int(retrieved_checks["id"]), checks.id)

        # Assert the file extensions of the retrieved
        # Checks match the created file extensions
        retrieved_allowed_file_extensions = retrieved_checks["allowed_file_extensions"]

        self.assertEqual(len(retrieved_allowed_file_extensions), 2)
        self.assertEqual(
            retrieved_allowed_file_extensions[0]["extension"], fileExtension1.extension
        )
        self.assertEqual(
            retrieved_allowed_file_extensions[1]["extension"], fileExtension4.extension
        )

        retrieved_forbidden_file_extensions = retrieved_checks[
            "forbidden_file_extensions"
        ]
        self.assertEqual(len(retrieved_forbidden_file_extensions), 2)
        self.assertEqual(
            retrieved_forbidden_file_extensions[0]["extension"],
            fileExtension2.extension,
        )
        self.assertEqual(
            retrieved_forbidden_file_extensions[1]["extension"],
            fileExtension3.extension,
        )
