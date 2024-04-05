import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from api.models.checks import StructureCheck, ExtraCheck
from api.models.extension import FileExtension
from api.models.project import Project
from api.models.course import Course
from django.conf import settings


def create_fileExtension(id, extension):
    """
    Create a FileExtension with the given arguments.
    """
    return FileExtension.objects.create(id=id, extension=extension)


def create_structure_check(id, name, project, obligated_extensions, blocked_extensions):
    """
    Create a StructureCheck with the given arguments.
    """
    check = StructureCheck.objects.create(id=id, name=name, project=project)

    for ext in obligated_extensions:
        check.obligated_extensions.add(ext)
    for ext in blocked_extensions:
        check.blocked_extensions.add(ext)

    return check


# def create_extra_check(id, project, run_script):
#     """
#     Create an ExtraCheck with the given arguments.
#     """
#     return ExtraCheck.objects.create(id=id, project=project, run_script=run_script)


def create_project(id, name, description, visible, archived, days, course, max_score, group_size):
    """Create a Project with the given arguments."""
    deadline = timezone.now() + timezone.timedelta(days=days)

    return Project.objects.create(
        id=id,
        name=name,
        description=description,
        visible=visible,
        archived=archived,
        deadline=deadline,
        course=course,
        max_score=max_score,
        group_size=group_size,
    )


def create_course(id, name, academic_startyear):
    """
    Create a Course with the given arguments.
    """
    return Course.objects.create(
        id=id, name=name, academic_startyear=academic_startyear
    )


def get_project():
    course = create_course(id=1, name="Course", academic_startyear=2021)
    project = create_project(
        id=1,
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

    def test_no_fileExtension(self):
        """
        Able to retrieve no FileExtension before publishing it.
        """
        response_root = self.client.get(reverse("file-extension-list"), follow=True)
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
        response = self.client.get(reverse("file-extension-list"), follow=True)

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
        response = self.client.get(reverse("file-extension-list"), follow=True)

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
            reverse("file-extension-detail", args=[str(fileExtension.id)]), follow=True
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
        fileExtension1 = create_fileExtension(id=1, extension="jpg")
        fileExtension2 = create_fileExtension(id=2, extension="png")
        fileExtension3 = create_fileExtension(id=3, extension="tar")
        fileExtension4 = create_fileExtension(id=4, extension="wfp")
        checks = create_structure_check(
            id=1,
            name=".",
            project=get_project(),
            obligated_extensions=[fileExtension1, fileExtension4],
            blocked_extensions=[fileExtension2, fileExtension3],
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
            retrieved_obligated_file_extensions[0]["extension"], fileExtension1.extension
        )
        self.assertEqual(
            retrieved_obligated_file_extensions[1]["extension"], fileExtension4.extension
        )

        retrieved_blocked_file_extensions = retrieved_checks[
            "blocked_extensions"
        ]
        self.assertEqual(len(retrieved_blocked_file_extensions), 2)
        self.assertEqual(
            retrieved_blocked_file_extensions[0]["extension"],
            fileExtension2.extension,
        )
        self.assertEqual(
            retrieved_blocked_file_extensions[1]["extension"],
            fileExtension3.extension,
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
#             id=1, project=get_project(), run_script="test.sh"
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
