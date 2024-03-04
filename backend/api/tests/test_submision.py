import json
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models.submission import Submission, SubmissionFile
from ..models.project import Project
from ..models.group import Group
from ..models.course import Course


def create_course(name, academic_startyear, description=None, parent_course=None):
    """
    Create a Course with the given arguments.
    """
    return Course.objects.create(
        name=name,
        academic_startyear=academic_startyear,
        description=description,
        parent_course=parent_course,
    )


def create_project(name, description, days, course):
    """Create a Project with the given arguments."""
    deadline = timezone.now() + timedelta(days=days)
    return Project.objects.create(
        name=name, description=description, deadline=deadline, course=course
    )


def create_group(project, score):
    """Create a Group with the given arguments."""
    return Group.objects.create(project=project, score=score)


def create_submission(group, submission_number):
    """Create an Submission with the given arguments."""
    return Submission.objects.create(
        group=group, submission_number=submission_number, submission_time=timezone.now()
    )


def create_submissionFile(submission, file):
    """Create an SubmissionFile with the given arguments."""
    return SubmissionFile.objects.create(submission=submission, file=file)


class SubmissionModelTests(TestCase):
    def test_no_submission(self):
        """
        able to retrieve no submission before publishing it.
        """

        response_root = self.client.get(reverse("submission-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")
        # Parse the JSON content from the response
        content_json = json.loads(response_root.content.decode("utf-8"))
        # Assert that the parsed JSON is an empty list
        self.assertEqual(content_json, [])

    def test_submission_exists(self):
        """
        Able to retrieve a single submission after creating it.
        """
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)
        submission = create_submission(group=group, submission_number=1)

        # Make a GET request to retrieve the submission
        response = self.client.get(reverse("submission-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one submission
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json[0]
        expected_group_url = "http://testserver" + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission.id)
        self.assertEqual(
            int(retrieved_submission["submission_number"]), submission.submission_number
        )
        self.assertEqual(retrieved_submission["group"], expected_group_url)

    def test_multiple_submission_exists(self):
        """
        Able to retrieve multiple submissions after creating them.
        """
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)
        submission1 = create_submission(group=group, submission_number=1)

        submission2 = create_submission(group=group, submission_number=2)

        # Make a GET request to retrieve the submission
        response = self.client.get(reverse("submission-list"), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one submission
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json[0]
        expected_group_url = "http://testserver" + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission1.id)
        self.assertEqual(
            int(retrieved_submission["submission_number"]),
            submission1.submission_number,
        )
        self.assertEqual(retrieved_submission["group"], expected_group_url)

        retrieved_submission = content_json[1]
        expected_group_url = "http://testserver" + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission2.id)
        self.assertEqual(
            int(retrieved_submission["submission_number"]),
            submission2.submission_number,
        )
        self.assertEqual(retrieved_submission["group"], expected_group_url)

    def test_submission_detail_view(self):
        """
        Able to retrieve details of a single submission.
        """
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)
        submission = create_submission(group=group, submission_number=1)

        # Make a GET request to retrieve the submission
        response = self.client.get(
            reverse("submission-detail", args=[str(submission.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json
        expected_group_url = "http://testserver" + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission.id)
        self.assertEqual(
            int(retrieved_submission["submission_number"]), submission.submission_number
        )
        self.assertEqual(retrieved_submission["group"], expected_group_url)

    def test_submission_group(self):
        """
        Able to retrieve group of a single submission.
        """
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)
        submission = create_submission(group=group, submission_number=1)

        # Make a GET request to retrieve the submission
        response = self.client.get(
            reverse("submission-detail", args=[str(submission.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json
        self.assertEqual(int(retrieved_submission["id"]), submission.id)
        self.assertEqual(
            int(retrieved_submission["submission_number"]), submission.submission_number
        )

        response = self.client.get(content_json["group"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        expected_project_url = "http://testserver" + reverse(
            "project-detail", args=[str(project.id)]
        )

        self.assertEqual(int(content_json["id"]), group.id)
        self.assertEqual(content_json["project"], expected_project_url)
        self.assertEqual(content_json["score"], group.score)
