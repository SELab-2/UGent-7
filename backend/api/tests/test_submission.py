import json

from api.tests.helpers import (create_course, create_group,
                               create_past_project, create_project,
                               create_submission)
from authentication.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.translation import gettext
from rest_framework.test import APITestCase
from ypovoli.settings import TESTING_BASE_LINK


class SubmissionModelTests(APITestCase):

    def setUp(self) -> None:
        self.client.force_authenticate(  # type: ignore
            User.get_dummy_admin()
        )

    def test_no_submission(self):
        """
        able to retrieve no submission before publishing it.
        """

        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )

        response_root = self.client.get(reverse("project-submissions", args=[str(project.id)]), follow=True)
        self.assertEqual(response_root.status_code, 200)
        # Assert that the response is JSON
        self.assertEqual(response_root.accepted_media_type, "application/json")  # type: ignore
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
        submission = create_submission(group=group, zip="zip1")

        # Make a GET request to retrieve the submission
        response = self.client.get(reverse("project-submissions", args=[str(project.id)]), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one submission
        self.assertEqual(len(content_json), 1)

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json[0]
        expected_group_url = TESTING_BASE_LINK + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission.id)
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
        submission1 = create_submission(group=group, zip="zip1")

        submission2 = create_submission(group=group, zip="zip2")

        # Make a GET request to retrieve the submission
        response = self.client.get(reverse("project-submissions", args=[str(project.id)]), follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with one submission
        self.assertEqual(len(content_json), 2)

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json[0]
        expected_group_url = TESTING_BASE_LINK + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission1.id)
        self.assertEqual(retrieved_submission["group"], expected_group_url)

        retrieved_submission = content_json[1]
        expected_group_url = TESTING_BASE_LINK + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission2.id)
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
        submission = create_submission(group=group, zip="zip1")

        # Make a GET request to retrieve the submission
        response = self.client.get(
            reverse("submission-detail", args=[str(submission.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json
        expected_group_url = TESTING_BASE_LINK + reverse(
            "group-detail", args=[str(group.id)]
        )
        self.assertEqual(int(retrieved_submission["id"]), submission.id)
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
        submission = create_submission(group=group, zip="zip1")

        # Make a GET request to retrieve the submission
        response = self.client.get(
            reverse("submission-detail", args=[str(submission.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json
        self.assertEqual(int(retrieved_submission["id"]), submission.id)

        response = self.client.get(content_json["group"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(int(content_json["id"]), group.id)
        self.assertEqual(content_json["score"], group.score)

    def test_submission_extra_checks(self):
        """
        Able to retrieve extra checks of a single submission.
        """
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)
        submission = create_submission(group=group, zip="zip1")

        # Make a GET request to retrieve the submission
        response = self.client.get(
            reverse("submission-detail", args=[str(submission.id)]), follow=True
        )

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert the details of the retrieved submission
        # match the created submission
        retrieved_submission = content_json
        self.assertEqual(int(retrieved_submission["id"]), submission.id)

    def test_submission_before_deadline(self):
        """
        Able to subbmit to a project before the deadline.
        """
        zip_file_path = "data/testing/tests/mixed.zip"

        with open(zip_file_path, 'rb') as file:
            files = {'files': SimpleUploadedFile('mixed.zip', file.read())}
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-submissions", args=[str(group.id)]),
            files,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

    def test_submission_after_deadline(self):
        """
        Not able to subbmit to a project after the deadline.
        """
        zip_file_path = "data/testing/tests/mixed.zip"

        with open(zip_file_path, 'rb') as f:
            files = {'files': SimpleUploadedFile('mixed.zip', f.read())}

        course = create_course(name="sel2", academic_startyear=2023)
        project = create_past_project(
            name="Project 1", description="Description 1", days=-7, course=course, days_start_date=-84
        )

        group = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-submissions", args=[str(group.id)]),
            files,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': [gettext("project.error.submissions.past_project")]})

    # def test_submission_number_increases_by_1(self):
    #     """
    #     When submiting a submission the submission number should be the prev one + 1
    #     """
    #     zip_file_path = "data/testing/tests/mixed.zip"

    #     with open(zip_file_path, 'rb') as f:
    #         files = {'files': SimpleUploadedFile('mixed.zip', f.read())}

    #     course = create_course(name="sel2", academic_startyear=2023)
    #     project = create_project(
    #         name="Project 1", description="Description 1", days=7, course=course
    #     )
    #     group = create_group(project=project, score=10)

    #     max_submission_number_before = group.submissions.aggregate(Max('submission_number'))['submission_number__max']

    #     if max_submission_number_before is None:
    #         max_submission_number_before = 0

    #     old_submissions = group.submissions.count()
    #     response = self.client.post(
    #         reverse("group-submissions", args=[str(group.id)]),
    #         files,
    #         follow=True,
    #     )

    #     group.refresh_from_db()
    #     new_submissions = group.submissions.count()

    #     max_submission_number_after = group.submissions.aggregate(Max('submission_number'))['submission_number__max']

    #     if max_submission_number_after is None:
    #         max_submission_number_after = 0
    #     self.assertEqual(max_submission_number_after - max_submission_number_before, 1)
    #     self.assertEqual(new_submissions - old_submissions, 1)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.accepted_media_type, "application/json")
    #     self.assertEqual(json.loads(response.content), {"message": gettext("group.success.submissions.add")})

    def test_submission_invisible_project(self):
        """
        Not able to subbmit to a project if its not visible.
        """
        zip_file_path = "data/testing/tests/mixed.zip"

        with open(zip_file_path, 'rb') as f:
            files = {'files': SimpleUploadedFile('mixed.zip', f.read())}

        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )

        project.toggle_visible()
        project.save()

        group = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-submissions", args=[str(group.id)]),
            files,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': [gettext("project.error.submissions.non_visible_project")]})

    def test_submission_archived_project(self):
        """
        Not able to subbmit to a project if its archived.
        """
        zip_file_path = "data/testing/tests/mixed.zip"

        with open(zip_file_path, 'rb') as f:
            files = {'files': SimpleUploadedFile('mixed.zip', f.read())}

        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )

        project.toggle_archived()
        project.save()

        group = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-submissions", args=[str(group.id)]),
            files,
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': [gettext("project.error.submissions.archived_project")]})
