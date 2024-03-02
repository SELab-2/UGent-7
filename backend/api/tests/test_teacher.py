import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models.teacher import Teacher


def create_teacher(id, first_name, last_name, email):
    # Create an Teacher with the given arguments.
    username = f"{first_name}_{last_name}"
    return Teacher.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )


class TeacherModelTests(TestCase):
    def test_no_teacher(self):
        """
        able to retrieve no teacher before publishing it.
        """

        response_root = self.client.get(reverse("teacher-list"), follow=True)
        # print(response.content)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_teacher_exists(self):
        """
        Able to retrieve a single teacher after creating it.
        """
        teacher = create_teacher(
            id=3,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )

        # Make a GET request to retrieve the teacher
        response = self.client.get(reverse("teacher-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one teacher
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved teacher match the created teacher
        retrieved_teacher = content_json[0]
        self.assertEqual(int(retrieved_teacher["id"]), teacher.id)
        self.assertEqual(
            retrieved_teacher["first_name"], teacher.first_name)
        self.assertEqual(retrieved_teacher["last_name"], teacher.last_name)
        self.assertEqual(retrieved_teacher["email"], teacher.email)

    def test_multiple_teachers(self):
        """
        Able to retrieve multiple teachers after creating them.
        """
        # Create multiple assistant
        teacher1 = create_teacher(
            id=1,
            first_name="Johny",
            last_name="Doeg",
            email="john.doe@example.com"
            )
        teacher2 = create_teacher(
            id=2,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com"
            )

        # Make a GET request to retrieve the teacher
        response = self.client.get(reverse("teacher-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple teacher
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved teacher match the created teacher
        retrieved_teacher1, retrieved_teacher2 = content_json
        self.assertEqual(int(retrieved_teacher1["id"]), teacher1.id)
        self.assertEqual(
            retrieved_teacher1["first_name"], teacher1.first_name)
        self.assertEqual(
            retrieved_teacher1["last_name"], teacher1.last_name)
        self.assertEqual(retrieved_teacher1["email"], teacher1.email)

        self.assertEqual(int(retrieved_teacher2["id"]), teacher2.id)
        self.assertEqual(
            retrieved_teacher2["first_name"], teacher2.first_name)
        self.assertEqual(
            retrieved_teacher2["last_name"], teacher2.last_name)
        self.assertEqual(retrieved_teacher2["email"], teacher2.email)

    def test_teacher_detail_view(self):
        """
        Able to retrieve details of a single teacher.
        """
        # Create an teacher for testing with the name "Bob Peeters"
        teacher = create_teacher(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com"
            )

        # Make a GET request to retrieve the teacher details
        response = self.client.get(
            reverse("teacher-detail", args=[str(teacher.id)]), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved teacher match the created teacher
        self.assertEqual(int(content_json["id"]), teacher.id)
        self.assertEqual(content_json["first_name"], teacher.first_name)
        self.assertEqual(content_json["last_name"], teacher.last_name)
        self.assertEqual(content_json["email"], teacher.email)