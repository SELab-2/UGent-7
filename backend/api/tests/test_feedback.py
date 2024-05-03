from rest_framework.test import APITestCase

from api.models.teacher import Teacher
from api.models.feedback import Feedback
from api.models.group import Group
from authentication.models import User
from api.tests.helpers import *


class FeedbackModelTestsAsTeacher(APITestCase):
    def setUp(self) -> None:
        self.user = Teacher.objects.create(
            id="teacher",
            first_name="Bobke",
            last_name="Peeters",
            username="bpeeters",
            email="Test@gmail.com"
        )

        self.client.force_authenticate(user=self.user)

    def test_create_feedback(self):
        course = create_course(name="sel2", academic_startyear=2023)
        course.teachers.add(self.user)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group: Group = create_group(project)
        submission: Submission = create_submission(1, group, True)
        """Test creating a feedback."""
        response = self.client.post(
            "/api/submissions/" + str(submission.id) + "/feedback/",
            {
                "message": "This is the feedback",
            },
            follow=True,
            )
