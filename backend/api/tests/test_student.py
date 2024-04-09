import json
from django.urls import reverse
from rest_framework.test import APITestCase
from api.models.student import Student
from api.tests.helpers import create_student, create_course, create_faculty, create_user
from authentication.models import User


class StudentModelTests(APITestCase):

    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_no_student(self):
        """
        Able to retrieve no student before publishing it.
        """

        response_root = self.client.get(reverse("student-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_activate_new(self):
        """Able to add a new student role to a user"""
        # Create the initial user
        user = create_user("1", "Saul", "Goodman", "saul@goodman.com")

        # Attempt to add the student role to the user
        response_root = self.client.post(
            reverse("student-list"),
            data={"user": user.id, "student_id": "02000341"},
            follow=True
        )

        # Assert a 200 status code
        self.assertEqual(response_root.status_code, 200)

        # Assert that an active student exists with the user ID
        self.assertTrue(Student.objects.filter(id=user.id, is_active=True).exists())

    def test_activate_old(self):
        """Able to re-activate an existing student role"""
        # Create the initial student, but don't activate
        student = create_student("1", "Saul", "Goodman", "saul@goodman.com", "02000341", False)

        # Attempt to add the student role to the user
        response_root = self.client.post(
            reverse("student-list"),
            data={"user": student.id, "student_id": "14300020"},
            follow=True
        )

        # Assert a 200 status code
        self.assertEqual(response_root.status_code, 200)

        # Assert that an active student exists with the user ID
        self.assertTrue(Student.objects.filter(id=student.id, is_active=True).exists())

        # Assert that the old student ID was kept
        self.assertTrue(Student.objects.filter(student_id=student.student_id).exists())

    def test_deactivate(self):
        """Able to deactivate an existing student role"""
        # Create the initial student
        student = create_student("1", "Saul", "Goodman", "saul@goodman.com", "02000341", True)

        # Attempt to remove the student role from the user
        response_root = self.client.delete(
            reverse("student-detail", args=[student.id]),
            data={"user": student.id, "student_id": "14300020"},
            follow=True
        )

        # Assert a 200 status code
        self.assertEqual(response_root.status_code, 200)

        # Assert that an active student with the user ID no longer exists
        self.assertFalse(Student.objects.filter(id=student.id, is_active=True).exists())

    def test_student_exists(self):
        """
        Able to retrieve a single student after creating it.
        """
        student = create_student(
            id=3, first_name="John", last_name="Doe", email="john.doe@example.com"
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
        self.assertEqual(retrieved_student["first_name"], student.first_name)
        self.assertEqual(retrieved_student["last_name"], student.last_name)
        self.assertEqual(retrieved_student["email"], student.email)

    def test_multiple_students(self):
        """
        Able to retrieve multiple students after creating them.
        """
        # Create multiple assistant
        student1 = create_student(
            id=1, first_name="Johny", last_name="Doe", email="john.doe@example.com", student_id="0100"
        )
        student2 = create_student(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", student_id="0200"
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
        self.assertEqual(retrieved_student1["first_name"], student1.first_name)
        self.assertEqual(retrieved_student1["last_name"], student1.last_name)
        self.assertEqual(retrieved_student1["email"], student1.email)

        self.assertEqual(int(retrieved_student2["id"]), student2.id)
        self.assertEqual(retrieved_student2["first_name"], student2.first_name)
        self.assertEqual(retrieved_student2["last_name"], student2.last_name)
        self.assertEqual(retrieved_student2["email"], student2.email)

    def test_student_detail_view(self):
        """
        Able to retrieve details of a single student.
        """
        # Create a student for testing with the name "Bob Peeters"
        student = create_student(
            id=5, first_name="Bob", last_name="Peeters", email="bob.peeters@example.com"
        )

        # Make a GET request to retrieve the student details
        response = self.client.get(
            reverse("student-detail", args=[str(student.id)]), follow=True
        )

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

    def test_student_faculty(self):
        """
        Able to retrieve faculty details of a single student.
        """
        # Create a student for testing with the name "Bob Peeters"
        faculty = create_faculty(name="testing faculty")
        student = create_student(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com",
            faculty=[faculty],
        )

        # Make a GET request to retrieve the student details
        response = self.client.get(
            reverse("student-detail", args=[str(student.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved student
        # match the created student
        self.assertEqual(int(content_json["id"]), student.id)
        self.assertEqual(content_json["first_name"], student.first_name)
        self.assertEqual(content_json["last_name"], student.last_name)
        self.assertEqual(content_json["email"], student.email)

        response = self.client.get(content_json["faculties"][0], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content_json["name"], faculty.name)

    def test_student_courses(self):
        """
        Able to retrieve courses details of a single student.
        """
        # Create a student for testing with the name "Bob Peeters"
        course1 = create_course(
            name="Introduction to Computer Science",
            academic_startyear=2022,
            description="An introductory course on computer science.",
        )
        course2 = create_course(
            name="Intermediate to Computer Science",
            academic_startyear=2023,
            description="An second course on computer science.",
        )

        student = create_student(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com",
            courses=[course1, course2],
        )

        # Make a GET request to retrieve the student details
        response = self.client.get(
            reverse("student-detail", args=[str(student.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved student
        # match the created student
        self.assertEqual(int(content_json["id"]), student.id)
        self.assertEqual(content_json["first_name"], student.first_name)
        self.assertEqual(content_json["last_name"], student.last_name)
        self.assertEqual(content_json["email"], student.email)

        response = self.client.get(content_json["courses"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple student
        self.assertEqual(len(content_json), 2)

        content = content_json[0]
        self.assertEqual(int(content["id"]), course1.id)
        self.assertEqual(content["name"], course1.name)
        self.assertEqual(int(content["academic_startyear"]), course1.academic_startyear)
        self.assertEqual(content["description"], course1.description)

        content = content_json[1]
        self.assertEqual(int(content["id"]), course2.id)
        self.assertEqual(content["name"], course2.name)
        self.assertEqual(int(content["academic_startyear"]), course2.academic_startyear)
        self.assertEqual(content["description"], course2.description)
