import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from api.models.project import Project
from api.models.course import Course
from api.models.checks import Checks, FileExtension


def create_course(id, name, academic_startyear):
    """
    Create a Course with the given arguments.
    """
    return Course.objects.create(
        id=id, name=name, academic_startyear=academic_startyear
    )


def create_fileExtension(id, extension):
    """
    Create a FileExtension with the given arguments.
    """
    return FileExtension.objects.create(id=id, extension=extension)


def create_checks(
    id=None, allowed_file_extensions=None, forbidden_file_extensions=None
):
    """Create a Checks with the given arguments."""
    if id is None and allowed_file_extensions is None:
        # extra if to make line shorter
        if forbidden_file_extensions is None:
            return Checks.objects.create()

    check = Checks.objects.create(
        id=id,
    )

    for ext in allowed_file_extensions:
        check.allowed_file_extensions.add(ext)
    for ext in forbidden_file_extensions:
        check.forbidden_file_extensions.add(ext)
    return check


def create_project(name, description, visible, archived, days, checks, course):
    """Create a Project with the given arguments."""
    deadline = timezone.now() + timezone.timedelta(days=days)

    return Project.objects.create(
        name=name,
        description=description,
        visible=visible,
        archived=archived,
        deadline=deadline,
        checks=checks,
        course=course,
    )


class ProjectModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_toggle_visible(self):
        """
        toggle the visible state of a project.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=-10,
            checks=checks,
            course=course,
        )
        self.assertIs(past_project.visible, True)
        past_project.toggle_visible()
        self.assertIs(past_project.visible, False)
        past_project.toggle_visible()
        self.assertIs(past_project.visible, True)

    def test_toggle_archived(self):
        """
        toggle the archived state of a project.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=True,
            days=-10,
            checks=checks,
            course=course,
        )

        self.assertIs(past_project.archived, True)
        past_project.toggle_archived()
        self.assertIs(past_project.archived, False)
        past_project.toggle_archived()
        self.assertIs(past_project.archived, True)

    def test_deadline_approaching_in_with_past_Project(self):
        """
        deadline_approaching_in() returns False for Projects whose Deadline
        is in the past.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=-10,
            checks=checks,
            course=course,
        )
        self.assertIs(past_project.deadline_approaching_in(), False)

    def test_deadline_approaching_in_with_future_Project_within_time(self):
        """
        deadline_approaching_in() returns True for Projects whose Deadline
        is in the timerange given.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        future_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=6,
            checks=checks,
            course=course,
        )
        self.assertIs(future_project.deadline_approaching_in(days=7), True)

    def test_deadline_approaching_in_with_future_Project_not_within_time(self):
        """
        deadline_approaching_in() returns False for Projects whose Deadline
        is out of the timerange given.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        future_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=8,
            checks=checks,
            course=course,
        )
        self.assertIs(future_project.deadline_approaching_in(days=7), False)

    def test_deadline_passed_with_future_Project(self):
        """
        deadline_passed() returns False for Projects whose Deadline
        is not passed.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        future_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=1,
            checks=checks,
            course=course,
        )
        self.assertIs(future_project.deadline_passed(), False)

    def test_deadline_passed_with_past_Project(self):
        """
        deadline_passed() returns True for Projects whose Deadline
        is passed.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=-1,
            checks=checks,
            course=course,
        )
        self.assertIs(past_project.deadline_passed(), True)

    def test_no_projects(self):
        """Able to retrieve no projects before creating any."""
        response = self.client.get(reverse("group-list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content_json, [])

    def test_project_exists(self):
        """
        Able to retrieve a single project after creating it.
        """

        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course,
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_project = content_json[0]

        expected_checks_url = "http://testserver" + reverse(
            "check-detail", args=[str(checks.id)]
        )

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)
        self.assertEqual(retrieved_project["checks"], expected_checks_url)
        self.assertEqual(retrieved_project["course"], expected_course_url)

    def test_multiple_project(self):
        """
        Able to retrieve multiple projects after creating it.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course,
        )

        project2 = create_project(
            name="test project2",
            description="test description2",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course,
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 2)

        retrieved_project = content_json[0]

        expected_checks_url = "http://testserver" + reverse(
            "check-detail", args=[str(checks.id)]
        )

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)
        self.assertEqual(retrieved_project["checks"], expected_checks_url)
        self.assertEqual(retrieved_project["course"], expected_course_url)

        retrieved_project = content_json[1]

        expected_checks_url = "http://testserver" + reverse(
            "check-detail", args=[str(checks.id)]
        )

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project2.name)
        self.assertEqual(retrieved_project["description"], project2.description)
        self.assertEqual(retrieved_project["visible"], project2.visible)
        self.assertEqual(retrieved_project["archived"], project2.archived)
        self.assertEqual(retrieved_project["checks"], expected_checks_url)
        self.assertEqual(retrieved_project["course"], expected_course_url)

    def test_project_course(self):
        """
        Able to retrieve a course of a project after creating it.
        """

        course = create_course(id=3, name="test course", academic_startyear=2024)
        checks = create_checks()
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course,
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_project = content_json[0]

        expected_checks_url = "http://testserver" + reverse(
            "check-detail", args=[str(checks.id)]
        )

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)
        self.assertEqual(retrieved_project["checks"], expected_checks_url)

        response = self.client.get(retrieved_project["course"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)

    def test_project_checks(self):
        """
        Able to retrieve a check of a project after creating it.
        """

        course = create_course(id=3, name="test course", academic_startyear=2024)
        fileExtension1 = create_fileExtension(id=1, extension="jpg")
        fileExtension2 = create_fileExtension(id=2, extension="png")
        fileExtension3 = create_fileExtension(id=3, extension="tar")
        fileExtension4 = create_fileExtension(id=4, extension="wfp")
        checks = create_checks(
            id=5,
            allowed_file_extensions=[fileExtension1, fileExtension4],
            forbidden_file_extensions=[fileExtension2, fileExtension3],
        )
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course,
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_project = content_json[0]

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)
        self.assertEqual(retrieved_project["course"], expected_course_url)

        response = self.client.get(retrieved_project["checks"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(int(content_json["id"]), checks.id)

        # Assert the file extensions of the retrieved
        # Checks match the created file extensions
        retrieved_allowed_file_extensions = content_json["allowed_file_extensions"]

        self.assertEqual(len(retrieved_allowed_file_extensions), 2)
        self.assertEqual(
            retrieved_allowed_file_extensions[0]["extension"], fileExtension1.extension
        )
        self.assertEqual(
            retrieved_allowed_file_extensions[1]["extension"], fileExtension4.extension
        )

        retrieved_forbidden_file_extensions = content_json["forbidden_file_extensions"]
        self.assertEqual(len(retrieved_forbidden_file_extensions), 2)
        self.assertEqual(
            retrieved_forbidden_file_extensions[0]["extension"],
            fileExtension2.extension,
        )
        self.assertEqual(
            retrieved_forbidden_file_extensions[1]["extension"],
            fileExtension3.extension,
        )
