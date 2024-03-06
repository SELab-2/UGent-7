import json
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from authentication.models import User
from api.models.project import Project
from api.models.student import Student
from api.models.group import Group
from api.models.course import Course


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


def create_student(id, first_name, last_name, email):
    """Create a Student with the given arguments."""
    username = f"{first_name}_{last_name}"
    return Student.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
    )


def create_group(project, score):
    """Create a Group with the given arguments."""
    return Group.objects.create(project=project, score=score)


class GroupModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_no_groups(self):
        """Able to retrieve no groups before creating any."""
        response = self.client.get(reverse("group-list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content_json, [])

    def test_group_exists(self):
        """Able to retrieve a single group after creating it."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )

        student = create_student(
            id=1, first_name="John", last_name="Doe", email="john.doe@example.com"
        )

        group = create_group(project=project, score=10)
        group.students.add(student)

        response = self.client.get(reverse("group-list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(content_json), 1)

        retrieved_group = content_json[0]
        expected_project_url = "http://testserver" + reverse(
            "project-detail", args=[str(project.id)]
        )

        self.assertEqual(retrieved_group["project"], expected_project_url)
        self.assertEqual(int(retrieved_group["id"]), group.id)
        self.assertEqual(retrieved_group["score"], group.score)

    def test_multiple_groups(self):
        """Able to retrieve multiple groups after creating them."""
        course = create_course(name="sel2", academic_startyear=2023)

        project1 = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        project2 = create_project(
            name="Project 2", description="Description 2", days=7, course=course
        )

        student1 = create_student(
            id=2, first_name="Bart", last_name="Rex", email="bart.rex@example.com"
        )
        student2 = create_student(
            id=3, first_name="Jane", last_name="Doe", email="jane.doe@example.com"
        )

        group1 = create_group(project=project1, score=10)
        group1.students.add(student1)

        group2 = create_group(project=project2, score=10)
        group2.students.add(student1, student2)

        response = self.client.get(reverse("group-list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(content_json), 2)

        retrieved_group1, retrieved_group2 = content_json
        expected_project_url1 = "http://testserver" + reverse(
            "project-detail", args=[str(project1.id)]
        )
        expected_project_url2 = "http://testserver" + reverse(
            "project-detail", args=[str(project2.id)]
        )

        self.assertEqual(retrieved_group1["project"], expected_project_url1)
        self.assertEqual(int(retrieved_group1["id"]), group1.id)
        self.assertEqual(retrieved_group1["score"], group1.score)

        self.assertEqual(retrieved_group2["project"], expected_project_url2)
        self.assertEqual(int(retrieved_group2["id"]), group2.id)
        self.assertEqual(retrieved_group2["score"], group2.score)

    def test_group_detail_view(self):
        """Able to retrieve details of a single group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student = create_student(
            id=5, first_name="John", last_name="Doe", email="john.doe@example.com"
        )

        group = create_group(project=project, score=10)
        group.students.add(student)

        response = self.client.get(
            reverse("group-detail", args=[str(group.id)]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        expected_project_url = "http://testserver" + reverse(
            "project-detail", args=[str(project.id)]
        )

        self.assertEqual(int(content_json["id"]), group.id)
        self.assertEqual(content_json["project"], expected_project_url)
        self.assertEqual(content_json["score"], group.score)

    def test_group_project(self):
        """Able to retrieve details of a single group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student = create_student(
            id=5, first_name="John", last_name="Doe", email="john.doe@example.com"
        )

        group = create_group(project=project, score=10)
        group.students.add(student)

        response = self.client.get(
            reverse("group-detail", args=[str(group.id)]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(int(content_json["id"]), group.id)
        self.assertEqual(content_json["score"], group.score)

        response = self.client.get(content_json["project"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        expected_course_url = "http://testserver" + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(content_json["name"], project.name)
        self.assertEqual(content_json["description"], project.description)
        self.assertEqual(content_json["visible"], project.visible)
        self.assertEqual(content_json["archived"], project.archived)
        self.assertEqual(content_json["course"], expected_course_url)

    def test_group_students(self):
        """Able to retrieve students details of a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student1 = create_student(
            id=5, first_name="John", last_name="Doe", email="john.doe@example.com"
        )

        student2 = create_student(
            id=6, first_name="kom", last_name="mor_up", email="kom.mor_up@example.com"
        )

        group = create_group(project=project, score=10)
        group.students.add(student1)
        group.students.add(student2)

        response = self.client.get(
            reverse("group-detail", args=[str(group.id)]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(int(content_json["id"]), group.id)
        self.assertEqual(content_json["score"], group.score)

        response = self.client.get(content_json["students"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(content_json), 2)

        content = content_json[0]
        self.assertEqual(int(content["id"]), student1.id)
        self.assertEqual(content["first_name"], student1.first_name)
        self.assertEqual(content["last_name"], student1.last_name)
        self.assertEqual(content["email"], student1.email)

        content = content_json[1]
        self.assertEqual(int(content["id"]), student2.id)
        self.assertEqual(content["first_name"], student2.first_name)
        self.assertEqual(content["last_name"], student2.last_name)
        self.assertEqual(content["email"], student2.email)
