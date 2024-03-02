import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models.student import Student


def create_student(id, first_name, last_name, email):
    # Create an student with the given arguments.
    username = f"{first_name}_{last_name}"
    return Student.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )


class StudentModelTests(TestCase):
    def test_no_student(self):
        """
        able to retrieve no student before publishing it.
        """

        response_root = self.client.get(reverse("student-list"), follow=True)
        # print(response.content)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_student_exists(self):
        """
        Able to retrieve a single student after creating it.
        """
        student = create_student(
            id=3,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )

        # Make a GET request to retrieve the student
        response = self.client.get(reverse("student-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one student
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved student match the created student
        retrieved_student = content_json[0]
        self.assertEqual(int(retrieved_student["id"]), student.id)
        self.assertEqual(
            retrieved_student["first_name"], student.first_name)
        self.assertEqual(retrieved_student["last_name"], student.last_name)
        self.assertEqual(retrieved_student["email"], student.email)

    def test_multiple_students(self):
        """
        Able to retrieve multiple students after creating them.
        """
        # Create multiple assistant
        student1 = create_student(
            id=1,
            first_name="Johny",
            last_name="Doeg",
            email="john.doe@example.com"
            )
        student2 = create_student(
            id=2,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com"
            )

        # Make a GET request to retrieve the student
        response = self.client.get(reverse("student-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple students
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved students
        # match the created students
        retrieved_student1, retrieved_student2 = content_json
        self.assertEqual(int(retrieved_student1["id"]), student1.id)
        self.assertEqual(
            retrieved_student1["first_name"], student1.first_name)
        self.assertEqual(
            retrieved_student1["last_name"], student1.last_name)
        self.assertEqual(retrieved_student1["email"], student1.email)

        self.assertEqual(int(retrieved_student2["id"]), student2.id)
        self.assertEqual(
            retrieved_student2["first_name"], student2.first_name)
        self.assertEqual(
            retrieved_student2["last_name"], student2.last_name)
        self.assertEqual(retrieved_student2["email"], student2.email)

    def test_student_detail_view(self):
        """
        Able to retrieve details of a single student.
        """
        # Create an student for testing with the name "Bob Peeters"
        student = create_student(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com"
            )

        # Make a GET request to retrieve the student details
        response = self.client.get(
            reverse("student-detail", args=[str(student.id)]), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved student match the created student
        self.assertEqual(int(content_json["id"]), student.id)
        self.assertEqual(content_json["first_name"], student.first_name)
        self.assertEqual(content_json["last_name"], student.last_name)
        self.assertEqual(content_json["email"], student.email)
