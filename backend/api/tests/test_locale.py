import json
from django.urls import reverse
from rest_framework.test import APITestCase

from api.models.course import Course
from api.models.student import Student
from authentication.models import User


class TestLocaleAddAlreadyPresentStudentToCourse(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(User.get_dummy_admin())

        course = Course.objects.create(id=1, name="Test Course", academic_startyear=2024)
        student = Student.objects.create(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")

        student.courses.add(course)

    def test_default_locale(self):
        response = self.client.post(reverse("course-students", args=["1"]),
                                    {"student_id": 1})

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(body["non_field_errors"][0], "The student is already present in the course.")

    def test_nl_locale(self):
        response = self.client.post(reverse("course-students", args=["1"]),
                                    {"student_id": 1},
                                    headers={"accept-language": "nl"})

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(body["non_field_errors"][0], "De student bevindt zich al in de opleiding.")
