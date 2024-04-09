import json
from django.urls import reverse
from rest_framework.test import APITestCase
from api.models.assistant import Assistant
from api.models.teacher import Teacher
from api.tests.helpers import create_faculty, create_course, create_assistant, create_user
from authentication.models import User


class AssistantModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_activate_new(self):
        """Able to add a new student role to a user"""
        # Create the initial user
        user = create_user("1", "Saul", "Goodman", "saul@goodman.com")

        # Attempt to add the student role to the user
        response_root = self.client.post(
            reverse("assistant-list"),
            data={"user": user.id},
            follow=True
        )

        # Assert a 200 status code
        self.assertEqual(response_root.status_code, 200)

        # Assert that an active student exists with the user ID
        self.assertTrue(Assistant.objects.filter(id=user.id, is_active=True).exists())

    def test_activate_old(self):
        """Able to re-activate an existing student role"""
        # Create the initial student, but don't activate
        assistant = create_assistant("1", "Saul", "Goodman", "saul@goodman.com", False)

        # Attempt to add the student role to the user
        response_root = self.client.post(
            reverse("assistant-list"),
            data={"user": assistant.id},
            follow=True
        )

        # Assert a 200 status code
        self.assertEqual(response_root.status_code, 200)

        # Assert that an active student exists with the user ID
        self.assertTrue(Assistant.objects.filter(id=assistant.id, is_active=True).exists())


    def test_deactivate(self):
        """Able to deactivate an existing student role"""
        # Create the initial student
        assistant = create_assistant("1", "Saul", "Goodman", "saul@goodman.com", True)

        # Attempt to remove the student role from the user
        response_root = self.client.delete(
            reverse("assistant-detail", args=[assistant.id]),
            data={"user": assistant.id},
            follow=True
        )

        # Assert a 200 status code
        self.assertEqual(response_root.status_code, 200)

        # Assert that an active student with the user ID no longer exists
        self.assertFalse(Assistant.objects.filter(id=assistant.id, is_active=True).exists())

    def test_no_assistant(self):
        """
        able to retrieve no assistant before publishing it.
        """

        response_root = self.client.get(reverse("assistant-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_assistant_exists(self):
        """
        Able to retrieve a single assistant after creating it.
        """
        assistant = create_assistant(
            id=3, first_name="John", last_name="Doe", email="john.doe@example.com"
        )

        # Make a GET request to retrieve the assistant
        response = self.client.get(reverse("assistant-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one assistant
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved assistant
        # match the created assistant
        retrieved_assistant = content_json[0]
        self.assertEqual(int(retrieved_assistant["id"]), assistant.id)
        self.assertEqual(retrieved_assistant["first_name"], assistant.first_name)
        self.assertEqual(retrieved_assistant["last_name"], assistant.last_name)
        self.assertEqual(retrieved_assistant["email"], assistant.email)

    def test_multiple_assistant(self):
        """
        Able to retrieve multiple assistant after creating them.
        """
        # Create multiple assistant
        assistant1 = create_assistant(
            id=1, first_name="Johny", last_name="Doeg", email="john.doe@example.com"
        )
        assistant2 = create_assistant(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com"
        )

        # Make a GET request to retrieve the assistant
        response = self.client.get(reverse("assistant-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple assistant
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved
        # assistant match the created assistant
        retrieved_assistant1, retrieved_assistant2 = content_json
        self.assertEqual(int(retrieved_assistant1["id"]), assistant1.id)
        self.assertEqual(retrieved_assistant1["first_name"], assistant1.first_name)
        self.assertEqual(retrieved_assistant1["last_name"], assistant1.last_name)
        self.assertEqual(retrieved_assistant1["email"], assistant1.email)

        self.assertEqual(int(retrieved_assistant2["id"]), assistant2.id)
        self.assertEqual(retrieved_assistant2["first_name"], assistant2.first_name)
        self.assertEqual(retrieved_assistant2["last_name"], assistant2.last_name)
        self.assertEqual(retrieved_assistant2["email"], assistant2.email)

    def test_assistant_detail_view(self):
        """
        Able to retrieve details of a single assistant.
        """
        # Create an assistant for testing with the name "Bob Peeters"
        assistant = create_assistant(
            id=5, first_name="Bob", last_name="Peeters", email="bob.peeters@example.com"
        )

        # Make a GET request to retrieve the assistant details
        response = self.client.get(
            reverse("assistant-detail", args=[str(assistant.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved assistant
        # match the created assistant
        self.assertEqual(int(content_json["id"]), assistant.id)
        self.assertEqual(content_json["first_name"], assistant.first_name)
        self.assertEqual(content_json["last_name"], assistant.last_name)
        self.assertEqual(content_json["email"], assistant.email)

    def test_assistant_faculty(self):
        """
        Able to retrieve faculty details of a single assistant.
        """
        # Create an assistant for testing with the name "Bob Peeters"
        faculty = create_faculty(name="testing faculty")
        assistant = create_assistant(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com",
            faculty=[faculty],
        )

        # Make a GET request to retrieve the assistant details
        response = self.client.get(
            reverse("assistant-detail", args=[str(assistant.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved assistant
        # match the created assistant
        self.assertEqual(int(content_json["id"]), assistant.id)
        self.assertEqual(content_json["first_name"], assistant.first_name)
        self.assertEqual(content_json["last_name"], assistant.last_name)
        self.assertEqual(content_json["email"], assistant.email)

        response = self.client.get(content_json["faculties"][0], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content_json["name"], faculty.name)

    def test_assistant_courses(self):
        """
        Able to retrieve courses details of a single assistant.
        """
        # Create an assistant for testing with the name "Bob Peeters"
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

        assistant = create_assistant(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com",
            courses=[course1, course2],
        )

        # Make a GET request to retrieve the assistant details
        response = self.client.get(
            reverse("assistant-detail", args=[str(assistant.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved assistant
        # match the created assistant
        self.assertEqual(int(content_json["id"]), assistant.id)
        self.assertEqual(content_json["first_name"], assistant.first_name)
        self.assertEqual(content_json["last_name"], assistant.last_name)
        self.assertEqual(content_json["email"], assistant.email)

        response = self.client.get(content_json["courses"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple assistant
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


class AssitantModelAsTeacherTests(APITestCase):
    def setUp(self) -> None:
        self.user = Teacher.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            username="john_doe",
            email="John.Doe@gmail.com"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_assistant_list(self):
        """
        Able to retrieve assistant list as a teacher.
        """
        # Create an assistant for testing with the name "Bob Peeters"
        create_assistant(
            id=5, first_name="Bob", last_name="Peeters", email="Bob.Peeters@gmail.com"
        )

        create_assistant(
            id=6, first_name="Jane", last_name="Doe", email="Jane.Doe@gmail.com"
        )

        # Make a GET request to retrieve the assistant details
        response = self.client.get(reverse("assistant-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple assistant
        self.assertEqual(len(content_json), 2)
