import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from api.models.project import Project
from api.models.course import Course
from api.models.group import Group
from api.models.submission import Submission
from api.models.teacher import Teacher
from api.models.student import Student
from api.models.checks import StructureCheck, ExtraCheck
from api.models.extension import FileExtension
from django.conf import settings


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


def create_group(project):
    """Create a Group with the given arguments."""

    return Group.objects.create(
        project=project,
    )


def create_submission(submission_number, group, structure_checks_passed):
    """Create a Submission with the given arguments."""

    return Submission.objects.create(
        submission_number=submission_number,
        group=group,
        structure_checks_passed=structure_checks_passed,
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

    def test_toggle_locked_groups(self):
        """
        toggle the locked state of the project groups.
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
        self.assertIs(past_project.locked_groups, False)
        past_project.toggle_groups_locked()
        self.assertIs(past_project.locked_groups, True)
        past_project.toggle_groups_locked()
        self.assertIs(past_project.locked_groups, False)


    def test_start_date_Project_not_in_past(self):
        """
        unable to create a project as a teacher/admin if the start date lies within the past.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        start_date = timezone.now() - timezone.timedelta(days=1)

        project_data = {
            "name": "Test Project",
            "description": "Test project description",
            "visible": True,
            "archived": False,
            "start_date": start_date,
            "deadline": timezone.now() + timezone.timedelta(days=1)
        }

        response = self.client.post(
            reverse("course-projects", args=[course.id]),
            data=project_data,
            follow=True
        )

        # Should not work since the start date lies in the past
        self.assertEqual(response.status_code, 400)


    def test_deadline_Project_before_start_date(self):
        """
        unable to create a project as a teacher/admin if the deadline lies before the start date.
        """
        course = create_course(id=3, name="test course", academic_startyear=2024)
        deadline = timezone.now() + timezone.timedelta(days=1)
        start_date = timezone.now() + timezone.timedelta(days=2)

        project_data = {
            "name": "Test Project",
            "description": "Test project description",
            "visible": True,
            "archived": False,
            "start_date": start_date,
            "deadline": deadline
        }

        response = self.client.post(
            reverse("course-projects", args=[course.id]),
            data=project_data,
            follow=True
        )

        # Should not work since deadline is before the start date
        self.assertEqual(response.status_code, 400)


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

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        retrieved_project = content_json

        expected_course_url = settings.TESTING_BASE_LINK + reverse(
            "course-detail", args=[str(course.id)]
        )

        self.assertEqual(retrieved_project["name"], project.name)
        self.assertEqual(retrieved_project["description"], project.description)
        self.assertEqual(retrieved_project["visible"], project.visible)
        self.assertEqual(retrieved_project["archived"], project.archived)
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

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        retrieved_project = content_json

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

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        retrieved_project = content_json

        expected_course_url = settings.TESTING_BASE_LINK + reverse(
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
        Able to retrieve an extra check of a project after creating it.
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

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        retrieved_project = content_json

        response = self.client.get(retrieved_project["extra_checks"], follow=True)

        # Check if the response was successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response is JSON
        self.assertEqual(response.accepted_media_type, "application/json")

        # Parse the JSON content from the response
        content_json = json.loads(response.content.decode("utf-8"))[0]

        self.assertEqual(int(content_json["id"]), checks.id)
        self.assertEqual(content_json["project"], settings.TESTING_BASE_LINK + reverse(
            "project-detail", args=[str(project.id)]
        ))
        self.assertEqual(content_json["run_script"], settings.TESTING_BASE_LINK + checks.run_script.url)


    def test_cant_join_locked_groups(self):
        """Should not be able to add a student to a group if the groups are locked."""
        course = create_course(id=3, name="sel2", academic_startyear=2023)

        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        # Create example students
        student1 = create_student(
            id=5, first_name="John", last_name="Doe", email="John.Doe@gmail.com"
        )
        student2 = create_student(
            id=7, first_name="Jane", last_name="Doe", email="Jane.Doe@gmail.com"
        )

        # Add these student to the course
        course.students.add(student1)
        course.students.add(student2)

        # Create an exmample group
        group = create_group(project=project)

        # Already add one student to the group
        group.students.add(student1)

        # Lock the groups
        project.locked_groups = True
        project.save()

        # Try to add a student to the group
        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": student2.id},
            follow=True,
        )

        # Should not work since the groups are locked
        self.assertEqual(response.status_code, 400)

        # Make sure the student is not in the group now
        self.assertFalse(group.students.filter(id=student2.id).exists())

        # Try to remove a student from the group
        response = self.client.post(
            reverse("group-students", args=[str(group.id)]),
            {"student_id": student1.id},
            follow=True,
        )

        # Make sure the student is still in the group now
        self.assertTrue(group.students.filter(id=student1.id).exists())



class ProjectModelTestsAsTeacher(APITestCase):
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

    def test_create_groups(self):
        """Able to create groups for a project."""
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.post(
            reverse("project-groups", args=[str(project.id)]),
            data={"number_groups": 3},
            follow=True,
        )

        # Make sure you cannot make groups for a project that is not yours
        self.assertEqual(response.status_code, 403)

        # Add the teacher to the course
        course.teachers.add(self.user)

        response = self.client.post(
            reverse("project-groups", args=[str(project.id)]),
            data={"number_groups": 3},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        # Assert that the groups were created
        self.assertEqual(project.groups.count(), 3)


    def test_submission_status_non_empty_groups(self):
        """Submission status returns the correct amount of non empty groups participating in the corresponding project."""
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(
            reverse("project-groups", args=[str(project.id)]),
            follow=True
        )

        # Make sure you cannot retrieve the submission status for a project that is not yours
        self.assertEqual(response.status_code, 403)

        # Add the teacher to the course
        course.teachers.add(self.user)

        # Create example students
        student1 = create_student(
            id=1, first_name="John", last_name="Doe", email="john.doe@example.com"
        )
        student2 = create_student(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com"
        )

        # Create example groups
        group1 = create_group(project=project)
        group2 = create_group(project=project)
        group3 = create_group(project=project)

        # Add the students to some of the groups
        group1.students.add(student1)
        group3.students.add(student2)

        response = self.client.get(
            reverse("project-submission-status", args=[str(project.id)]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        # Only two of the three created groups contain at least one student
        self.assertEqual(response.data, {
            "non_empty_groups": 2,
            "groups_submitted": 0,
            "submissions_passed": 0
        })


    def test_submission_status_groups_submitted_and_passed_checks(self):
        """Retrieve the submission status for a project."""
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(
            reverse("project-groups", args=[str(project.id)]),
            follow=True
        )

        # Make sure you cannot retrieve the submission status for a project that is not yours
        self.assertEqual(response.status_code, 403)

        # Add the teacher to the course
        course.teachers.add(self.user)

        # Create example students
        student1 = create_student(
            id=1, first_name="John", last_name="Doe", email="john.doe@example.com"
        )
        student2 = create_student(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com"
        )
        student3 = create_student(
            id=3, first_name="Joe", last_name="Doe", email="Joe.doe@example.com"
        )

        # Create example groups
        group1 = create_group(project=project)
        group2 = create_group(project=project)
        group3 = create_group(project=project)

        # Add students to the groups
        group1.students.add(student1)
        group2.students.add(student2)
        group3.students.add(student3)

        # Create submissions for certain groups
        create_submission(submission_number=1, group=group1, structure_checks_passed=True)
        create_submission(submission_number=2, group=group3, structure_checks_passed=False)

        response = self.client.get(
            reverse("project-submission-status", args=[str(project.id)]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "non_empty_groups": 3,
            "groups_submitted": 2,
            "submissions_passed": 1
        })


class ProjectModelTestsAsStudent(APITestCase):
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

    def test_try_to_create_groups(self):
        """Not able to create groups for a project."""
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )
        course.students.add(self.user)

        response = self.client.post(
            reverse("project-groups", args=[str(project.id)]),
            data={"number_groups": 3},
            follow=True,
        )

        # Make sure you cannot make groups as a student
        self.assertEqual(response.status_code, 403)
