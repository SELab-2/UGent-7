import json
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models.project import Project
from ..models.course import Course
from ..models.checks import Checks


def create_course(id, name, academic_startyear):
    return Course.objects.create(
        id=id, name=name, academic_startyear=academic_startyear)


def create_checks():
    return Checks.objects.create()


def create_project(
    name,
    description,
    visible,
    archived,
    days,
    checks,
    course
):
    deadline = timezone.now() + timezone.timedelta(days=days)

    return Project.objects.create(
        name=name,
        description=description,
        visible=visible,
        archived=archived,
        deadline=deadline,
        checks=checks,
        course=course
    )


class ProjectModelTests(TestCase):
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
        course = create_course(
            id=1,
            name="test course",
            academic_startyear=2024
            )
        checks = create_checks()

        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course
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
        # self.assertEqual(retrieved_project["checks"], expected_checks_url)
        self.assertEqual(retrieved_project["course"], expected_course_url)

    def test_multiple_project(self):
        """
        Able to retrieve multiple projects after creating it.
        """
        course = create_course(
            id=1,
            name="test course",
            academic_startyear=2024
            )

        checks = create_checks()

        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course
            )

        project2 = create_project(
            name="test project2",
            description="test description2",
            visible=True,
            archived=False,
            days=7,
            checks=checks,
            course=course
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
        # TODO
        # self.assertEqual(retrieved_project["checks"], expected_checks_url)
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
        # TODO
        # self.assertEqual(retrieved_project["checks"], expected_checks_url)
        self.assertEqual(retrieved_project["course"], expected_course_url)
