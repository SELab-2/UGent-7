import json

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext
from rest_framework.test import APITestCase
from api.models.checks import ExtraCheck, StructureCheck
from api.models.project import Project
from api.models.student import Student
from api.models.teacher import Teacher
from api.tests.helpers import create_course, create_file_extension, create_project, create_group, create_submission, \
    create_student, create_structure_check
from authentication.models import User


class ProjectModelTests(APITestCase):
    def setUp(self) -> None:
        self.client.force_authenticate(User.get_dummy_admin())

    def test_toggle_visible(self):
        """
        toggle the visible state of a project.
        """
        course = create_course(name="test course", academic_startyear=2024)
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
        course = create_course(name="test course", academic_startyear=2024)
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
        course = create_course(name="test course", academic_startyear=2024)
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

    def test_automatically_create_groups_when_creating_project(self):
        """
        creating a project as a teacher should open the same amount of groups as students enrolled in the project.
        """
        course = create_course(name="test course", academic_startyear=2024)

        student1 = create_student(
            id=1, first_name="John", last_name="Doe", email="john.doe@example.com", student_id="0200"
        )
        student2 = create_student(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", student_id="0300"
        )
        student1.courses.add(course)
        student2.courses.add(course)

        project_data = {
            "name": "Test Project",
            "description": "Test project description",
            "visible": True,
            "archived": False,
            "start_date": timezone.now(),
            "deadline": timezone.now() + timezone.timedelta(days=1),
        }

        response = self.client.post(
            reverse("course-projects", args=[course.id]), data=project_data, follow=True
        )

        # Creating a group as a teacher should work
        self.assertEqual(response.status_code, 200)

        project = Project.objects.get(
            name="Test Project",
            description="Test project description",
            visible=True,
            archived=False,
            start_date=project_data["start_date"],
            deadline=project_data["deadline"],
            course=course,
        )

        groups_count = project.groups.count()
        # The amount of students participating in the corresponding course
        expected_groups_count = 2

        # We expect the amount of groups to be the same as the amount of students in the course
        self.assertEqual(groups_count, expected_groups_count)

    def test_start_date_Project_not_in_past(self):
        """
        unable to create a project as a teacher/admin if the start date lies within the past.
        """
        course = create_course(name="test course", academic_startyear=2024)
        start_date = timezone.now() - timezone.timedelta(days=1)

        project_data = {
            "name": "Test Project",
            "description": "Test project description",
            "visible": True,
            "archived": False,
            "start_date": start_date,
            "deadline": timezone.now() + timezone.timedelta(days=1),
        }

        response = self.client.post(
            reverse("course-projects", args=[course.id]), data=project_data, follow=True
        )

        # Should not work since the start date lies in the past
        self.assertEqual(response.status_code, 400)

    def test_deadline_Project_before_start_date(self):
        """
        unable to create a project as a teacher/admin if the deadline lies before the start date.
        """
        course = create_course(name="test course", academic_startyear=2024)
        deadline = timezone.now() + timezone.timedelta(days=1)
        start_date = timezone.now() + timezone.timedelta(days=2)

        project_data = {
            "name": "Test Project",
            "description": "Test project description",
            "visible": True,
            "archived": False,
            "start_date": start_date,
            "deadline": deadline,
        }

        response = self.client.post(
            reverse("course-projects", args=[course.id]), data=project_data, follow=True
        )

        # Should not work since deadline is before the start date
        self.assertEqual(response.status_code, 400)

    def test_deadline_approaching_in_with_past_Project(self):
        """
        deadline_approaching_in() returns False for Projects whose Deadline
        is in the past.
        """
        course = create_course(name="test course", academic_startyear=2024)
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
        course = create_course(name="test course", academic_startyear=2024)
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
        course = create_course(name="test course", academic_startyear=2024)
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
        course = create_course(name="test course", academic_startyear=2024)
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
        course = create_course(name="test course", academic_startyear=2024)
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

        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]), follow=True
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

        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]), follow=True
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

        course = create_course(name="test course", academic_startyear=2024)
        file_extension1 = create_file_extension(extension="jpg")
        file_extension2 = create_file_extension(extension="png")
        file_extension3 = create_file_extension(extension="tar")
        file_extension4 = create_file_extension(extension="wfp")
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )
        checks = create_structure_check(
            name=".",
            project=project,
            obligated_extensions=[file_extension1, file_extension4],
            blocked_extensions=[file_extension2, file_extension3],
        )

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]), follow=True
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
            retrieved_obligated_extensions[0]["extension"], file_extension1.extension
        )
        self.assertEqual(
            retrieved_obligated_extensions[1]["extension"], file_extension4.extension
        )

        retrieved_blocked_file_extensions = content_json["blocked_extensions"]
        self.assertEqual(len(retrieved_blocked_file_extensions), 2)
        self.assertEqual(
            retrieved_blocked_file_extensions[0]["extension"],
            file_extension2.extension,
        )
        self.assertEqual(
            retrieved_blocked_file_extensions[1]["extension"],
            file_extension3.extension,
        )

    def test_project_structure_checks_post(self):
        """
        Able to retrieve a structure check of a project after posting it.
        """

        course = create_course(name="test course", academic_startyear=2024)
        file_extension1 = create_file_extension(extension="jpg")
        file_extension2 = create_file_extension(extension="png")
        file_extension3 = create_file_extension(extension="tar")
        file_extension4 = create_file_extension(extension="wfp")
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.post(
            reverse("project-structure-checks", args=[str(project.id)]),
            {
                "name": ".",
                "obligated_extensions": [file_extension1.extension, file_extension4.extension],
                "blocked_extensions": [file_extension2.extension, file_extension3.extension]},
            follow=True,
        )

        project.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")
        self.assertEqual(json.loads(response.content), {'message': gettext('project.success.structure_check.add')})

        upd: StructureCheck = project.structure_checks.all()[0]
        retrieved_obligated_extensions = upd.obligated_extensions.all()
        retrieved_blocked_file_extensions = upd.blocked_extensions.all()

        self.assertEqual(len(retrieved_obligated_extensions), 2)
        self.assertEqual(
            retrieved_obligated_extensions[0].extension, file_extension1.extension
        )
        self.assertEqual(
            retrieved_obligated_extensions[1].extension, file_extension4.extension
        )

        self.assertEqual(len(retrieved_blocked_file_extensions), 2)
        self.assertEqual(
            retrieved_blocked_file_extensions[0].extension,
            file_extension2.extension,
        )
        self.assertEqual(
            retrieved_blocked_file_extensions[1].extension,
            file_extension3.extension,
        )

    def test_project_structure_checks_post_already_existing(self):
        """
        Able to retrieve a structure check of a project after posting it.
        """

        course = create_course(name="test course", academic_startyear=2024)
        file_extension1 = create_file_extension(extension="jpg")
        file_extension2 = create_file_extension(extension="png")
        file_extension3 = create_file_extension(extension="tar")
        file_extension4 = create_file_extension(extension="wfp")
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        create_structure_check(
            name=".",
            project=project,
            obligated_extensions=[file_extension1, file_extension4],
            blocked_extensions=[file_extension2, file_extension3],
        )

        response = self.client.post(
            reverse("project-structure-checks", args=[str(project.id)]),
            {
                "name": ".",
                "obligated_extensions": [file_extension1.extension, file_extension4.extension],
                "blocked_extensions": [file_extension2.extension, file_extension3.extension]},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.accepted_media_type, "application/json")
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': [gettext("project.error.structure_checks.already_existing")]})

    def test_project_structure_checks_post_blocked_and_obligated(self):
        """
        Able to retrieve a structure check of a project after posting it.
        """

        course = create_course(name="test course", academic_startyear=2024)
        file_extension1 = create_file_extension(extension="jpg")
        file_extension2 = create_file_extension(extension="png")
        file_extension3 = create_file_extension(extension="tar")
        file_extension4 = create_file_extension(extension="wfp")
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.post(
            reverse("project-structure-checks", args=[str(project.id)]),
            {
                "name": ".",
                "obligated_extensions": [file_extension1.extension, file_extension4.extension],
                "blocked_extensions": [file_extension1.extension, file_extension2.extension,
                                       file_extension3.extension]},
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.accepted_media_type, "application/json")
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': [gettext("project.error.structure_checks.extension_blocked_and_obligated")]})

    # def test_project_extra_checks(self):
    #     """
    #     Able to retrieve an extra check of a project after creating it.
    #     """
    #     course = create_course(id=3, name="test course", academic_startyear=2024)
    #     project = create_project(
    #         name="test project",
    #         description="test description",
    #         visible=True,
    #         archived=False,
    #         days=7,
    #         course=course,
    #     )
    #     checks = ExtraCheck.objects.create(
    #         id=5,
    #         project=project,
    #         run_script="testscript.sh",
    #     )

    #     response = self.client.get(
    #         reverse("project-detail", args=[str(project.id)]), follow=True
    #     )

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.accepted_media_type, "application/json")

    #     content_json = json.loads(response.content.decode("utf-8"))

    #     retrieved_project = content_json

    #     response = self.client.get(retrieved_project["extra_checks"], follow=True)

    #     # Check if the response was successful
    #     self.assertEqual(response.status_code, 200)

    #     # Assert that the response is JSON
    #     self.assertEqual(response.accepted_media_type, "application/json")

    #     # Parse the JSON content from the response
    #     content_json = json.loads(response.content.decode("utf-8"))[0]

    #     self.assertEqual(int(content_json["id"]), checks.id)
    #     self.assertEqual(
    #         content_json["project"],
    #         settings.TESTING_BASE_LINK + reverse("project-detail", args=[str(project.id)]),
    #     )
    #     self.assertEqual(
    #         content_json["run_script"],
    #         settings.TESTING_BASE_LINK + checks.run_script.url,
    #     )

    def test_project_groups(self):
        """
        Able to retrieve a list of groups of a project after creating it.
        """
        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        group1 = create_group(project=project, score=0)
        group2 = create_group(project=project, score=0)

        response = self.client.get(
            reverse("project-groups", args=[str(project.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 2)

        self.assertEqual(int(content_json[0]["id"]), group1.id)
        self.assertEqual(int(content_json[1]["id"]), group2.id)

    def test_project_submissions(self):
        """
        Able to retrieve a list of submissions of a project after creating it.
        """
        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test project",
            description="test description",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        group1 = create_group(project=project, score=0)
        group2 = create_group(project=project, score=0)

        submission1 = create_submission(submission_number=1, group=group1, structure_checks_passed=True)
        submission2 = create_submission(submission_number=2, group=group2, structure_checks_passed=False)

        response = self.client.get(
            reverse("project-submissions", args=[str(project.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 2)

        self.assertEqual(int(content_json[0]["id"]), submission1.id)
        self.assertEqual(int(content_json[1]["id"]), submission2.id)

    def test_cant_join_locked_groups(self):
        """Should not be able to add a student to a group if the groups are locked."""
        course = create_course(name="sel2", academic_startyear=2023)

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
            id=5, first_name="John", last_name="Doe", email="John.Doe@gmail.com", student_id="1"
        )
        student2 = create_student(
            id=7, first_name="Jane", last_name="Doe", email="Jane.Doe@gmail.com", student_id="2"
        )

        # Add these student to the course
        course.students.add(student1)
        course.students.add(student2)

        # Create an example group
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
        self.client.post(
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
            email="Test@gmail.com",
        )

        self.client.force_authenticate(self.user)

    def test_create_groups(self):
        """Able to create groups for a project."""
        course = create_course(name="test course", academic_startyear=2024)
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
        """Submission status returns the correct amount of non empty groups participating in the project."""
        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(
            reverse("project-groups", args=[str(project.id)]), follow=True
        )

        # Make sure you cannot retrieve the submission status for a project that is not yours
        self.assertEqual(response.status_code, 403)

        # Add the teacher to the course
        course.teachers.add(self.user)

        # Create example students
        student1 = create_student(
            id=1, first_name="John", last_name="Doe", email="john.doe@example.com", student_id="0100"
        )
        student2 = create_student(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", student_id="0200"
        )

        # Create example groups
        group1 = create_group(project=project)
        group2 = create_group(project=project)
        group3 = create_group(project=project)  # noqa: F841

        # Add the students to some of the groups
        group1.students.add(student1)
        group2.students.add(student2)

        response = self.client.get(
            reverse("project-submission-status", args=[str(project.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)

        # Only two of the three created groups contain at least one student
        self.assertEqual(
            response.data,
            {"non_empty_groups": 2, "groups_submitted": 0, "submissions_passed": 0},
        )

    def test_submission_status_groups_submitted_and_passed_checks(self):
        """Retrieve the submission status for a project."""
        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )

        response = self.client.get(
            reverse("project-groups", args=[str(project.id)]), follow=True
        )

        # Make sure you cannot retrieve the submission status for a project that is not yours
        self.assertEqual(response.status_code, 403)

        # Add the teacher to the course
        course.teachers.add(self.user)

        # Create example students
        student1 = create_student(
            id=1, first_name="John", last_name="Doe", email="john.doe@example.com", student_id="0100"
        )
        student2 = create_student(
            id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", student_id="0200"
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
        create_submission(
            submission_number=1, group=group1, structure_checks_passed=True
        )
        create_submission(
            submission_number=2, group=group3, structure_checks_passed=False
        )

        response = self.client.get(
            reverse("project-submission-status", args=[str(project.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"non_empty_groups": 3, "groups_submitted": 2, "submissions_passed": 1},
        )

    def test_retrieve_list_submissions(self):
        """Able to retrieve a list of submissions for a project."""
        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=7,
            course=course,
        )
        course.teachers.add(self.user)

        group = create_group(project=project)

        create_submission(
            submission_number=1, group=group, structure_checks_passed=True
        )

        response = self.client.get(
            reverse("project-submissions", args=[str(project.id)]), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)


class ProjectModelTestsAsStudent(APITestCase):
    def setUp(self) -> None:
        self.user = Student.objects.create(
            id="student",
            first_name="Bobke",
            last_name="Peeters",
            username="bpeeters",
            email="Bobke.Peeters@gmail.com",
        )

        self.client.force_authenticate(self.user)

    def test_try_to_create_groups(self):
        """Not able to create groups for a project."""
        course = create_course(name="test course", academic_startyear=2024)
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
