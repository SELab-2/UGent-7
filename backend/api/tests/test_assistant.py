import json

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from api.models.assistant import Assistant


def create_assistant(id, first_name, last_name, email):
    # Create an Assistant with the given arguments.
    username = f"{first_name}_{last_name}"
    return Assistant.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )


class AssistantModelTests(TestCase):
    def test_no_assistant(self):
        """
        able to retrieve no assistant before publishing it.
        """

        response_root = self.client.get(reverse("assistant-list"), follow=True)
        # print(response.content)
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
            id=3,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )

        # Make a GET request to retrieve the assistant
        response = self.client.get(reverse("assistant-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one student
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved student match the created student
        retrieved_assistant = content_json[0]
        self.assertEqual(int(retrieved_assistant["id"]), assistant.id)
        self.assertEqual(
            retrieved_assistant["first_name"], assistant.first_name)
        self.assertEqual(retrieved_assistant["last_name"], assistant.last_name)
        self.assertEqual(retrieved_assistant["email"], assistant.email)

    def test_multiple_assistant(self):
        """
        Able to retrieve multiple assistant after creating them.
        """
        # Create multiple assistant
        assistant1 = create_assistant(
            id=1,
            first_name="Johny",
            last_name="Doeg",
            email="john.doe@example.com"
            )
        assistant2 = create_assistant(
            id=2,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com"
            )

        # Make a GET request to retrieve the assistant
        response = self.client.get(reverse("assistant-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple students
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved
        # students match the created students
        retrieved_assistant1, retrieved_assistant2 = content_json
        self.assertEqual(int(retrieved_assistant1["id"]), assistant1.id)
        self.assertEqual(
            retrieved_assistant1["first_name"], assistant1.first_name)
        self.assertEqual(
            retrieved_assistant1["last_name"], assistant1.last_name)
        self.assertEqual(retrieved_assistant1["email"], assistant1.email)

        self.assertEqual(int(retrieved_assistant2["id"]), assistant2.id)
        self.assertEqual(
            retrieved_assistant2["first_name"], assistant2.first_name)
        self.assertEqual(
            retrieved_assistant2["last_name"], assistant2.last_name)
        self.assertEqual(retrieved_assistant2["email"], assistant2.email)

    def test_assistant_detail_view(self):
        """
        Able to retrieve details of a single assistant.
        """
        # Create an student for testing with the name "Bob Peeters"
        assistant = create_assistant(
            id=5,
            first_name="Bob",
            last_name="Peeters",
            email="bob.peeters@example.com"
            )

        # Make a GET request to retrieve the assistant details
        response = self.client.get(
            reverse("assistant-detail", args=[str(assistant.id)]), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved student match the created student
        self.assertEqual(int(content_json["id"]), assistant.id)
        self.assertEqual(content_json["first_name"], assistant.first_name)
        self.assertEqual(content_json["last_name"], assistant.last_name)
        self.assertEqual(content_json["email"], assistant.email)
