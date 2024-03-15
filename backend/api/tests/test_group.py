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
from django.conf import settings
from api.models.teacher import Teacher


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


def create_project(name, description, days, course, group_size=2, max_score=20, score_visible=True):
    """Create a Project with the given arguments."""
    deadline = timezone.now() + timedelta(days=days)
    return Project.objects.create(
        name=name, description=description, deadline=deadline, course=course,
        group_size=group_size, max_score=max_score, score_visible=score_visible
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

        expected_project_url = settings.TESTING_BASE_LINK + reverse(
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

        expected_course_url = settings.TESTING_BASE_LINK + reverse(
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


class GroupModelTestsAsTeacher(APITestCase):
    def setUp(self) -> None:
        self.user = Teacher.objects.create(
            id="teacher",
            first_name="Bobke",
            last_name="Peeters",
            username="bpeeters",
            email="Test@gmail.com"
        )

        self.client.force_authenticate(
            self.user
        )

    def test_assign_student_to_group(self):
        """Able to assign a student to a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student = create_student(
            id=5, first_name="John", last_name="Doe", email="John.Doe@gmail.com"
        )

        # Add this teacher and student to the course
        course.teachers.add(self.user)
        course.students.add(student)

        group = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": student.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        # Make sure the student is in the group now
        self.assertTrue(group.students.filter(id=student.id).exists())

    def test_remove_student_from_group(self):
        """Able to remove a student from a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student = create_student(
            id=5, first_name="John", last_name="Doe", email="John.Doe@gmail.com"
        )

        # Add this teacher to the course
        course.teachers.add(self.user)

        group = create_group(project=project, score=10)
        group.students.add(student)

        response = self.client.delete(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": student.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        # Make sure the student is not in the group anymore
        self.assertFalse(group.students.filter(id=student.id).exists())

    def test_update_score_of_group(self):
        """Able to update the score of a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course, max_score=20
        )

        # Add this teacher to the course
        course.teachers.add(self.user)

        group = create_group(project=project, score=10)

        response = self.client.patch(
            reverse("group-detail", args=[str(group.id)]),
            {"score": 20},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        # Make sure the score of the group is updated
        group.refresh_from_db()
        self.assertEqual(group.score, 20)

        # Try to update the score of a group to a score higher than the maximum score
        response = self.client.patch(
            reverse("group-detail", args=[str(group.id)]),
            {"score": 30},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)

        # Make sure the score of the group is not updated
        group.refresh_from_db()
        self.assertEqual(group.score, 20)


class GroupModelTestsAsStudent(APITestCase):
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

    def test_join_group(self):
        """Able to join a group as a student."""
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)

        # Try to join a group that is part of a course the student is not enrolled in
        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        # Make sure that you can not join a group if you are not enrolled in the course
        self.assertEqual(response.status_code, 403)

        # Add the student to the course
        course.students.add(self.user)

        # Join the group now that the student is enrolled in the course
        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        # Make sure the student is in the group now
        self.assertTrue(group.students.filter(id=self.user.id).exists())

        # Try to join a second group
        group2 = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-students", args=[str(group2.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        # Make sure you can only be in one group at a time
        self.assertEqual(response.status_code, 400)

    def test_join_full_group(self):
        """Not able to join a full group as a student."""
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course, group_size=1
        )
        group = create_group(project=project, score=10)
        student = create_student(
            id=5, first_name="Bernard", last_name="Doe", email="Bernard.Doe@gmail.com"
        )
        group.students.add(student)

        # Add the student to the course
        course.students.add(self.user)

        # Join the group
        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)

    def test_leave_group(self):
        """Able to leave a group as a student."""
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)

        # Add the student to the course
        course.students.add(self.user)

        # Join the group
        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        # Make sure the student is in the group now
        self.assertTrue(group.students.filter(id=self.user.id).exists())

        # Leave the group
        response = self.client.delete(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        # Make sure the student is not in the group anymore
        self.assertFalse(group.students.filter(id=self.user.id).exists())

    def test_try_leave_locked_group(self):
        """Not able to leave a locked group as a student."""
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)
        project.locked_groups = True
        project.save()

        # Add the student to the course
        course.students.add(self.user)
        group.students.add(self.user)

        # Try to leave the group
        response = self.client.delete(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        # Make sure that you are not able to leave a locked group
        self.assertEqual(response.status_code, 400)

    def test_try_leave_group_not_part_of(self):
        """Not able to leave a group you are not part of as a student."""
        course = create_course(name="sel2", academic_startyear=2023)
        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        group = create_group(project=project, score=10)

        # Add the student to the course
        course.students.add(self.user)

        # Try to leave the group
        response = self.client.delete(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": self.user.id},
            follow=True,
        )

        # Make sure that you are not able to leave a group you are not part of
        self.assertEqual(response.status_code, 400)

    def test_try_to_assign_other_student_to_group(self):
        """Not able to assign another student to a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student = create_student(
            id=5, first_name="John", last_name="Doe", email="John.Doe@gmail.com"
        )

        # Add this student to the course
        course.students.add(student)
        course.students.add(self.user)

        group = create_group(project=project, score=10)

        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": student.id},
            follow=True,
        )

        # Make sure that you are not able to assign another student to a group
        self.assertEqual(response.status_code, 403)

    def test_try_to_delete_other_student_from_group(self):
        """Not able to remove another student from a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )
        student = create_student(
            id=5, first_name="John", last_name="Doe", email="John.Doe@gmail.com"
        )

        # Add this student to the course
        course.students.add(student)
        course.students.add(self.user)

        group = create_group(project=project, score=10)
        group.students.add(student)
        group.students.add(self.user)

        response = self.client.delete(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": student.id},
            follow=True,
        )

        # Make sure that you are not able to remove another student from a group
        self.assertEqual(response.status_code, 403)

    def test_try_to_update_score_of_group(self):
        """Not able to update the score of a group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course
        )

        # Add this student to the course
        course.students.add(self.user)

        group = create_group(project=project, score=10)
        group.students.add(self.user)

        response = self.client.patch(
            reverse("group-detail", args=[str(group.id)]),
            {"score": 20},
            follow=True,
        )

        # Make sure that you are not able to update the score of a group
        self.assertEqual(response.status_code, 403)

        group.refresh_from_db()
        self.assertEqual(group.score, 10)

    def test_group_score_visibility(self):
        """Only able to retrieve the score of a group if it is visible, and the student is part of the group."""
        course = create_course(name="sel2", academic_startyear=2023)

        project = create_project(
            name="Project 1", description="Description 1", days=7, course=course, score_visible=True
        )
        group = create_group(project=project, score=10)
        course.students.add(self.user)

        response = self.client.get(
            reverse("group-detail", args=[str(group.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)

        content_json = json.loads(response.content.decode("utf-8"))

        # Make sure that score is not included, because the student is not part of the group
        self.assertNotIn("score", content_json)

        # Add the student to the group
        group.students.add(self.user)

        # Set the visibility of the score to False, to make sure the score is not included if it is not visible
        project.score_visible = False
        project.save()

        response = self.client.get(
            reverse("group-detail", args=[str(group.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)

        content_json = json.loads(response.content.decode("utf-8"))

        # Make sure that score is not included, because the teacher has set the visibility of the score to False
        self.assertNotIn("score", content_json)

        # Update that the score is visible
        project.score_visible = True
        project.save()

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("group-detail", args=[str(group.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        content_json = json.loads(response.content.decode("utf-8"))

        # Make sure the score is included now
        self.assertIn("score", content_json)
