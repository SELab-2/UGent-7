import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from api.models.course import Course
from api.models.teacher import Teacher
from api.models.assistant import Assistant
from api.models.student import Student
from api.models.project import Project


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


def create_student(id, first_name, last_name, email):
    """
    Create a student with the given arguments.
    """
    username = f"{first_name}_{last_name}"
    student = Student.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )
    return student


def create_assistant(id, first_name, last_name, email):
    """
    Create a assistant with the given arguments.
    """
    username = f"{first_name}_{last_name}"
    assistant = Assistant.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )
    return assistant


def create_teacher(id, first_name, last_name, email):
    """
    Create a teacher with the given arguments.
    """
    username = f"{first_name}_{last_name}"
    teacher = Teacher.objects.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        create_time=timezone.now(),
    )
    return teacher


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


class CourseModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(
            User.get_dummy_admin()
        )

    def test_no_courses(self):
        """
        Able to retrieve no courses before publishing any.
        """
        response_root = self.client.get(reverse("course-list"), follow=True)
        self.assertEqual(response_root.status_code, 200)
        self.assertEqual(response_root.accepted_media_type, "application/json")
        content_json = json.loads(response_root.content.decode("utf-8"))
        self.assertEqual(content_json, [])

    def test_course_exists(self):
        """
        Able to retrieve a single course after creating it.
        """
        course = create_course(
            name="Introduction to Computer Science",
            academic_startyear=2022,
            description="An introductory course on computer science.",
        )

        response = self.client.get(reverse("course-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_course = content_json[0]
        self.assertEqual(retrieved_course["name"], course.name)
        self.assertEqual(
            retrieved_course["academic_startyear"], course.academic_startyear
        )
        self.assertEqual(retrieved_course["description"], course.description)

    def test_multiple_courses(self):
        """
        Able to retrieve multiple courses after creating them.
        """
        course1 = create_course(
            name="Mathematics 101",
            academic_startyear=2022,
            description="A basic mathematics course.",
        )
        course2 = create_course(
            name="Physics 101",
            academic_startyear=2022,
            description="An introductory physics course.",
        )

        response = self.client.get(reverse("course-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 2)

        retrieved_course1, retrieved_course2 = content_json
        self.assertEqual(retrieved_course1["name"], course1.name)
        self.assertEqual(
            retrieved_course1["academic_startyear"], course1.academic_startyear
        )
        self.assertEqual(retrieved_course1["description"], course1.description)

        self.assertEqual(retrieved_course2["name"], course2.name)
        self.assertEqual(
            retrieved_course2["academic_startyear"], course2.academic_startyear
        )
        self.assertEqual(retrieved_course2["description"], course2.description)

    def test_course_detail_view(self):
        """
        Able to retrieve details of a single course.
        """
        course = create_course(
            name="Chemistry 101",
            academic_startyear=2022,
            description="An introductory chemistry course.",
        )

        response = self.client.get(
            reverse("course-detail", args=[str(course.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)

    def test_course_teachers(self):
        """
        Able to retrieve teachers details of a single course.
        """
        teacher1 = create_teacher(
            id=5,
            first_name="Simon",
            last_name="Mignolet",
            email="simon.mignolet@ugent.be",
        )

        teacher2 = create_teacher(
            id=6, first_name="Ronny", last_name="Deila", email="ronny.deila@brugge.be"
        )

        course = create_course(
            name="Chemistry 101",
            academic_startyear=2022,
            description="An introductory chemistry course.",
        )
        course.teachers.add(teacher1)
        course.teachers.add(teacher2)

        response = self.client.get(
            reverse("course-detail", args=[str(course.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)

        response = self.client.get(content_json["teachers"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple teachers
        self.assertEqual(len(content_json), 2)

        content = content_json[0]
        self.assertEqual(int(content["id"]), teacher1.id)
        self.assertEqual(content["first_name"], teacher1.first_name)
        self.assertEqual(content["last_name"], teacher1.last_name)
        self.assertEqual(content["email"], teacher1.email)

        content = content_json[1]
        self.assertEqual(int(content["id"]), teacher2.id)
        self.assertEqual(content["first_name"], teacher2.first_name)
        self.assertEqual(content["last_name"], teacher2.last_name)
        self.assertEqual(content["email"], teacher2.email)

    def test_course_assistant(self):
        """
        Able to retrieve assistant details of a single course.
        """
        assistant1 = create_assistant(
            id=5,
            first_name="Simon",
            last_name="Mignolet",
            email="simon.mignolet@ugent.be",
        )

        assistant2 = create_assistant(
            id=6, first_name="Ronny", last_name="Deila", email="ronny.deila@brugge.be"
        )

        course = create_course(
            name="Chemistry 101",
            academic_startyear=2022,
            description="An introductory chemistry course.",
        )
        course.assistants.add(assistant1)
        course.assistants.add(assistant2)

        response = self.client.get(
            reverse("course-detail", args=[str(course.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)

        response = self.client.get(content_json["assistants"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple teachers
        self.assertEqual(len(content_json), 2)

        content = content_json[0]
        self.assertEqual(int(content["id"]), assistant1.id)
        self.assertEqual(content["first_name"], assistant1.first_name)
        self.assertEqual(content["last_name"], assistant1.last_name)
        self.assertEqual(content["email"], assistant1.email)

        content = content_json[1]
        self.assertEqual(int(content["id"]), assistant2.id)
        self.assertEqual(content["first_name"], assistant2.first_name)
        self.assertEqual(content["last_name"], assistant2.last_name)
        self.assertEqual(content["email"], assistant2.email)

    def test_course_student(self):
        """
        Able to retrieve student details of a single course.
        """
        student1 = create_student(
            id=5,
            first_name="Simon",
            last_name="Mignolet",
            email="simon.mignolet@ugent.be",
        )

        student2 = create_student(
            id=6, first_name="Ronny", last_name="Deila", email="ronny.deila@brugge.be"
        )

        course = create_course(
            name="Chemistry 101",
            academic_startyear=2022,
            description="An introductory chemistry course.",
        )
        course.students.add(student1)
        course.students.add(student2)

        response = self.client.get(
            reverse("course-detail", args=[str(course.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)

        response = self.client.get(content_json["students"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple student
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

    def test_course_project(self):
        """
        Able to retrieve project details of a single course.
        """
        course = create_course(
            name="Chemistry 101",
            academic_startyear=2022,
            description="An introductory chemistry course.",
        )

        project1 = create_project(
            name="become champions",
            description="win the jpl",
            visible=True,
            archived=False,
            days=50,
            course=course,
        )

        project2 = create_project(
            name="become european champion",
            description="win the cfl",
            visible=True,
            archived=False,
            days=50,
            course=course,
        )

        response = self.client.get(
            reverse("course-detail", args=[str(course.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)

        response = self.client.get(content_json["projects"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))

        # Assert that the parsed JSON is a list with multiple projects
        self.assertEqual(len(content_json), 2)

        content = content_json[0]
        self.assertEqual(int(content["id"]), project1.id)
        self.assertEqual(content["name"], project1.name)
        self.assertEqual(content["description"], project1.description)
        self.assertEqual(content["visible"], project1.visible)
        self.assertEqual(content["archived"], project1.archived)

        content = content_json[1]
        self.assertEqual(int(content["id"]), project2.id)
        self.assertEqual(content["name"], project2.name)
        self.assertEqual(content["description"], project2.description)
        self.assertEqual(content["visible"], project2.visible)
        self.assertEqual(content["archived"], project2.archived)
