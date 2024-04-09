import json
from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from api.tests.helpers import create_structure_check, create_file_extension, create_project, create_course


def get_project():
    course = create_course(name="Course", academic_startyear=2021)

    project = create_project(
        name="Project",
        description="Description",
        visible=True,
        archived=False,
        days=5,
        course=course,
        max_score=10,
        group_size=2,
    )
    return project


class FileExtensionModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_no_file_extension(self):
        """
        Able to retrieve no file_extension before publishing it.
        """
        response_root = self.client.get(reverse("file-extension-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_file_extension_exists(self):
        """
        Able to retrieve a single file_extension after creating it.
        """
        file_extension = create_file_extension(extension="pdf")

        # Make a GET request to retrieve the file_extension
        response = self.client.get(reverse("file-extension-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one file_extension
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved file_extension
        # match the created file_extension
        retrieved_file_extension = content_json[0]
        self.assertEqual(retrieved_file_extension["extension"], file_extension.extension)

    def test_multiple_file_extension(self):
        """
        Able to retrieve multiple file_extension after creating them.
        """
        # Create multiple file_extension
        file_extension1 = create_file_extension(extension="jpg")
        file_extension2 = create_file_extension(extension="png")

        # Make a GET request to retrieve the file_extension
        response = self.client.get(reverse("file-extension-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple file_extension
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved file_extension
        # match the created file_extension
        retrieved_file_extension1, retrieved_file_extension2 = content_json
        self.assertEqual(
            retrieved_file_extension1["extension"], file_extension1.extension
        )

        self.assertEqual(
            retrieved_file_extension2["extension"], file_extension2.extension
        )

    def test_file_extension_detail_view(self):
        """
        Able to retrieve details of a single file_extension.
        """
        # Create an file_extension for testing.
        file_extension = create_file_extension(extension="zip")

        # Make a GET request to retrieve the file_extension details
        response = self.client.get(
            reverse("file-extension-detail", args=[str(file_extension.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved file_extension
        # match the created file_extension
        self.assertEqual(content_json["extension"], file_extension.extension)


class StructureCheckModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_no_checks(self):
        """
        Able to retrieve no Checks before publishing it.
        """
        response_root = self.client.get(reverse("structure-check-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        self.assertEqual(response_root.accepted_media_type, "application/json")
        content_json = json.loads(response_root.content.decode("utf-8"))
        self.assertEqual(content_json, [])

    def test_structure_checks_exists(self):
        """
        Able to retrieve a single Checks after creating it.
        """
        # Create a Checks instance with some file extensions
        file_extension1 = create_file_extension(extension="jpg")
        file_extension2 = create_file_extension(extension="png")
        file_extension3 = create_file_extension(extension="tar")
        file_extension4 = create_file_extension(extension="wfp")
        checks = create_structure_check(
            name=".",
            project=get_project(),
            obligated_extensions=[file_extension1, file_extension4],
            blocked_extensions=[file_extension2, file_extension3],
        )

        # Make a GET request to retrieve the Checks
        response = self.client.get(reverse("structure-check-list"), follow=True)

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
        retrieved_obligated_file_extensions = retrieved_checks["obligated_extensions"]

        self.assertEqual(len(retrieved_obligated_file_extensions), 2)
        self.assertEqual(
            retrieved_obligated_file_extensions[0]["extension"], file_extension1.extension
        )
        self.assertEqual(
            retrieved_obligated_file_extensions[1]["extension"], file_extension4.extension
        )

        retrieved_blocked_file_extensions = retrieved_checks[
            "blocked_extensions"
        ]
        self.assertEqual(len(retrieved_blocked_file_extensions), 2)
        self.assertEqual(
            retrieved_blocked_file_extensions[0]["extension"],
            file_extension2.extension,
        )
        self.assertEqual(
            retrieved_blocked_file_extensions[1]["extension"],
            file_extension3.extension,
        )


# class ExtraCheckModelTests(APITestCase):
#     def setUp(self) -> None:
#         self.client.force_authenticate(
#             User.get_dummy_admin()
#         )

#     def test_no_checks(self):
#         """
#         Able to retrieve no Checks before publishing it.
#         """
#         response_root = self.client.get(reverse("extra-check-list"), follow=True)
#         self.assertEqual(response_root.status_code, 200)
#         self.assertEqual(response_root.accepted_media_type, "application/json")
#         content_json = json.loads(response_root.content.decode("utf-8"))
#         self.assertEqual(content_json, [])

#     def test_extra_checks_exists(self):
#         """
#         Able to retrieve a single Checks after creating it.
#         """
#         checks = create_extra_check(
#              project=get_project(), run_script="test.sh"
#         )

#         # Make a GET request to retrieve the Checks
#         response = self.client.get(reverse("extra-check-list"), follow=True)

#         # Check if the response was successful
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.accepted_media_type, "application/json")

#         # Parse the JSON content from the response
#         content_json = json.loads(response.content.decode("utf-8"))

#         # Assert that the parsed JSON is a list with one Checks
#         self.assertEqual(len(content_json), 1)

#         # Assert the details of the retrieved Checks match the created Checks
#         retrieved_checks = content_json[0]
#         self.assertEqual(int(retrieved_checks["id"]), checks.id)
#         self.assertEqual(retrieved_checks["run_script"], settings.TESTING_BASE_LINK + checks.run_script.url)
