import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from api.models.project import Project
from api.models.course import Course
from api.models.checks import StructureCheck, ExtraCheck
from api.models.extension import FileExtension


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


def create_project(name, description, visible, archived, days, course):
    """Create a Project with the given arguments."""
    deadline = timezone.now() + timezone.timedelta(days=days)

    return Project.objects.create(
        name=name,
        description=description,
        visible=visible,
        archived=archived,
        deadline=deadline,
        course=course,
    )


def create_structure_check(id, name, project, obligated_extensions, blocked_extensions):
    """
    Create a StructureCheck with the given arguments.
    """
    check = StructureCheck.objects.create(id=id, name=name, project=project)

    for ext in obligated_extensions:
        check.obligated_extensions.add(ext)
    for ext in blocked_extensions:
        check.blocked_extensions.add(ext)

    return check


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
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=-10,
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
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=True,
            days=-10,
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
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=-10,
            course=course,
        )
        self.assertIs(past_project.deadline_approaching_in(), False)

    def test_deadline_approaching_in_with_future_Project_within_time(self):
        """
        deadline_approaching_in() returns True for Projects whose Deadline
        is in the timerange given.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        future_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=6,
            course=course,
        )
        self.assertIs(future_project.deadline_approaching_in(days=7), True)

    def test_deadline_approaching_in_with_future_Project_not_within_time(self):
        """
        deadline_approaching_in() returns False for Projects whose Deadline
        is out of the timerange given.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        future_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=8,
            course=course,
        )
        self.assertIs(future_project.deadline_approaching_in(days=7), False)

    def test_deadline_passed_with_future_Project(self):
        """
        deadline_passed() returns False for Projects whose Deadline
        is not passed.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        future_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=1,
            course=course,
        )
        self.assertIs(future_project.deadline_passed(), False)

    def test_deadline_passed_with_past_Project(self):
        """
        deadline_passed() returns True for Projects whose Deadline
        is passed.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        past_project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=-1,
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
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
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

    def test_multiple_project(self):
        """
        Able to retrieve multiple projects after creating it.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        project2 = create_project(
            name="test project2",
            description="test description2",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 2)

        retrieved_project = content_json[0]

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)
        self.assertEqual(retrieved_project["course"], expected_course_url)

        retrieved_project = content_json[1]

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project2.name)
        self.assertEqual(retrieved_project["description"], project2.description)
        self.assertEqual(retrieved_project["visible"], project2.visible)
        self.assertEqual(retrieved_project["archived"], project2.archived)
        self.assertEqual(retrieved_project["course"], expected_course_url)

    def test_project_course(self):
        """
        Able to retrieve a course of a project after creating it.
        """

        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_project = content_json[0]

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)

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

    def test_project_structure_checks(self):
        """
        Able to retrieve a structure check of a project after creating it.
        """

        course = create_course(id=3, name="test course", academic_startyear=2024)
        fileExtension1 = create_fileExtension(id=1, extension="jpg")
        fileExtension2 = create_fileExtension(id=2, extension="png")
        fileExtension3 = create_fileExtension(id=3, extension="tar")
        fileExtension4 = create_fileExtension(id=4, extension="wfp")
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )
        checks = create_structure_check(
            id=5,
            name=".",
            project=project,
            obligated_extensions=[fileExtension1, fileExtension4],
            blocked_extensions=[fileExtension2, fileExtension3],
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

        response = self.client.get(retrieved_project["structure_checks"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))[0]

        self.assertEqual(int(content_json["id"]), checks.id)

        # Assert the file extensions of the retrieved
        # Checks match the created file extensions
        retrieved_obligated_extensions = content_json["obligated_extensions"]

        self.assertEqual(len(retrieved_obligated_extensions), 2)
        self.assertEqual(
            retrieved_obligated_extensions[0]["extension"], fileExtension1.extension
        )
        self.assertEqual(
            retrieved_obligated_extensions[1]["extension"], fileExtension4.extension
        )

        retrieved_blocked_file_extensions = content_json["blocked_extensions"]
        self.assertEqual(len(retrieved_blocked_file_extensions), 2)
        self.assertEqual(
            retrieved_blocked_file_extensions[0]["extension"],
            fileExtension2.extension,
        )
        self.assertEqual(
            retrieved_blocked_file_extensions[1]["extension"],
            fileExtension3.extension,
        )

    def test_project_extra_checks(self):
        """
        Able to retrieve a extra check of a project after creating it.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )
        checks = ExtraCheck.objects.create(
            id=5,
            project=project,
            run_script="testscript.sh",
        )

        response = self.client.get(reverse("project-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_project = content_json[0]

        response = self.client.get(retrieved_project["extra_checks"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))[0]

        self.assertEqual(int(content_json["id"]), checks.id)
        self.assertEqual(content_json["project"], "http://testserver" + reverse(
            "project-detail", args=[str(project.id)]
        ))
        self.assertEqual(content_json["run_script"], "http://testserver" + checks.run_script.url)
