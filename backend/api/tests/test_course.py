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


def get_course():
    """
    Return a random course to use in tests.
    """
    return create_course(name="Chemistry 101", academic_startyear=2023, description="An introductory chemistry course.")


def get_assistant():
    """
    Return a random assistant to use in tests.
    """
    return create_assistant(id=5, first_name="Simon", last_name="Mignolet", email="Simon.Mignolet@gmail.com")


def get_student():
    """
    Return a random student to use in tests.
    """
    return create_student(id=5, first_name="Simon", last_name="Mignolet", email="Simon.Mignolet@gmai.com")


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


class CourseModelTestsAsStudent(APITestCase):
    def setUp(self) -> None:
        self.user = Student.objects.create(
            id="student",
            first_name="Bobke",
            last_name="Peeters",
            username="bpeeters",
            email="Bobke.Peeters@gmail.com"
        )

        self.client.force_authenticate(
            self.user
        )

    def test_try_add_assistant(self):
        """
        Students should not be able to add assistants.
        """
        course = get_course()
        course.students.add(self.user)

        assistant = get_assistant()

        response = self.client.post(
            reverse("course-assistants", args=[str(course.id)]),
            data={"assistant": assistant.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(course.assistants.filter(id=assistant.id).exists())

    def test_try_remove_assistant(self):
        """
        Students should not be able to remove assistants.
        """
        course = get_course()
        course.students.add(self.user)

        assistant = get_assistant()

        course.assistants.add(assistant)

        response = self.client.delete(
            reverse("course-assistants", args=[str(course.id)]),
            data={"assistant": assistant.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(course.assistants.filter(id=assistant.id).exists())

    def test_add_self_to_course(self):
        """
        Able to add self to a course.
        """
        course = get_course()

        response = self.client.post(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(course.students.filter(id=self.user.id).exists())

    def test_remove_self_from_course(self):
        """
        Able to remove self from a course.
        """
        course = get_course()
        course.students.add(self.user)

        response = self.client.delete(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(course.students.filter(id=self.user.id).exists())

    def test_try_add_other_student_to_course(self):
        """
        Students should not be able to add other students to a course.
        """
        course = get_course()
        course.students.add(self.user)

        other_student = get_student()

        response = self.client.post(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": other_student.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(course.students.filter(id=other_student.id).exists())

    def test_try_remove_other_student_from_course(self):
        """
        Students should not be able to remove other students from a course.
        """
        course = get_course()
        course.students.add(self.user)

        other_student = get_student()

        course.students.add(other_student)

        response = self.client.delete(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": other_student.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(course.students.filter(id=other_student.id).exists())

    def test_try_create_course(self):
        """
        Students should not be able to create a course.
        """
        response = self.client.post(
            reverse("course-list"),
            data={
                "name": "Introduction to Computer Science",
                "academic_startyear": 2022,
                "description": "An introductory course on computer science.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            Course.objects.filter(name="Introduction to Computer Science").exists()
        )

    def test_try_create_project(self):
        """
        Students should not be able to create a project.
        """
        course = get_course()
        course.students.add(self.user)

        response = self.client.post(
            reverse("course-projects", args=[str(course.id)]),
            data={
                "name": "become champions",
                "description": "win the jpl",
                "visible": True,
                "archived": False,
                "days": 50,
                "deadline": timezone.now() + timezone.timedelta(days=50),
                "start_date": timezone.now()
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(course.projects.filter(name="become champions").exists())

    def test_try_join_old_year_course(self):
        """
        Students should not be able to join a course from a previous year.
        """
        course = get_course()
        course.academic_startyear = 2020
        course.save()

        response = self.client.post(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)

        self.assertFalse(course.students.filter(id=self.user.id).exists())

    def test_try_leave_old_year_course(self):
        """
        Students should not be able to leave a course from a previous year.
        """
        course = get_course()
        course.academic_startyear = 2020
        course.save()

        course.students.add(self.user)

        response = self.client.delete(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)

        self.assertTrue(course.students.filter(id=self.user.id).exists())

    def test_try_leave_course_not_part_of(self):
        """
        Students should not be able to leave a course they are not part of.
        """
        course = get_course()

        response = self.client.delete(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)

        self.assertFalse(course.students.filter(id=self.user.id).exists())


class CourseModelTestsAsTeacher(APITestCase):
    def setUp(self) -> None:
        self.user = Teacher.objects.create(
            id="teacher",
            first_name="Bobke",
            last_name="Peeters",
            username="bpeeters",
            email="Bobke.Peeters@gmail.com"
        )

        self.client.force_authenticate(
            self.user
        )

    def test_add_assistant(self):
        """
        Able to add an assistant to a course.
        """
        course = get_course()
        course.teachers.add(self.user)

        assistant = get_assistant()

        response = self.client.post(
            reverse("course-assistants", args=[str(course.id)]),
            data={"assistant": assistant.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(course.assistants.filter(id=assistant.id).exists())

    def test_remove_assistant(self):
        """
        Able to remove an assistant from a course.
        """
        course = get_course()
        course.teachers.add(self.user)

        assistant = get_assistant()

        course.assistants.add(assistant)

        response = self.client.delete(
            reverse("course-assistants", args=[str(course.id)]),
            data={"assistant": assistant.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(course.assistants.filter(id=assistant.id).exists())

    def test_add_student(self):
        """
        Able to add a student to a course.
        """
        course = get_course()
        course.teachers.add(self.user)

        student = get_student()

        response = self.client.post(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": student.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(course.students.filter(id=student.id).exists())

    def test_remove_student(self):
        """
        Able to remove a student from a course.
        """
        course = get_course()
        course.teachers.add(self.user)

        student = get_student()

        course.students.add(student)

        response = self.client.delete(
            reverse("course-students", args=[str(course.id)]),
            data={"student_id": student.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(course.students.filter(id=student.id).exists())

    def test_create_course(self):
        """
        Able to create a course.
        """
        response = self.client.post(
            reverse("course-list"),
            data={
                "name": "Introduction to Computer Science",
                "academic_startyear": 2022,
                "description": "An introductory course on computer science.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Course.objects.filter(name="Introduction to Computer Science").exists()
        )

    def test_create_project(self):
        """
        Able to create a project for a course.
        """
        course = get_course()
        course.teachers.add(self.user)

        response = self.client.post(
            reverse("course-projects", args=[str(course.id)]),
            data={
                "name": "become champions",
                "description": "win the jpl",
                "visible": True,
                "archived": False,
                "days": 50,
                "deadline": timezone.now() + timezone.timedelta(days=50),
                "start_date": timezone.now()
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(course.projects.filter(name="become champions").exists())

    def test_clone_course(self):
        """
        Able to clone a course.
        """
        course = get_course()
        course.teachers.add(self.user)

        response = self.client.post(
            reverse("course-clone", args=[str(course.id)]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(name=course.name,
                                              academic_startyear=course.academic_startyear + 1).exists())
