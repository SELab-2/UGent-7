import json

from django.test import TestCase
from django.urls import reverse
from ..models.course import Course


def create_course(name, academic_startyear, description=None,
                  parent_course=None):
    """
    Create a Course with the given arguments.
    """
    return Course.objects.create(
        name=name,
        academic_startyear=academic_startyear,
        description=description,
        parent_course=parent_course
    )


class CourseModelTests(TestCase):
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
            description="An introductory course on computer science."
        )

        response = self.client.get(reverse("course-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 1)

        retrieved_course = content_json[0]
        self.assertEqual(retrieved_course["name"], course.name)
        self.assertEqual(
            retrieved_course["academic_startyear"], course.academic_startyear)
        self.assertEqual(retrieved_course["description"], course.description)

    def test_multiple_courses(self):
        """
        Able to retrieve multiple courses after creating them.
        """
        course1 = create_course(
            name="Mathematics 101",
            academic_startyear=2022,
            description="A basic mathematics course."
        )
        course2 = create_course(
            name="Physics 101",
            academic_startyear=2022,
            description="An introductory physics course."
        )

        response = self.client.get(reverse("course-list"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 2)

        retrieved_course1, retrieved_course2 = content_json
        self.assertEqual(retrieved_course1["name"], course1.name)
        self.assertEqual(
            retrieved_course1["academic_startyear"],
            course1.academic_startyear)
        self.assertEqual(retrieved_course1["description"], course1.description)

        self.assertEqual(retrieved_course2["name"], course2.name)
        self.assertEqual(
            retrieved_course2["academic_startyear"],
            course2.academic_startyear)
        self.assertEqual(retrieved_course2["description"], course2.description)

    def test_course_detail_view(self):
        """
        Able to retrieve details of a single course.
        """
        course = create_course(
            name="Chemistry 101",
            academic_startyear=2022,
            description="An introductory chemistry course."
        )

        response = self.client.get(
            reverse("course-detail", args=[str(course.id)]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content_json["name"], course.name)
        self.assertEqual(
            content_json["academic_startyear"], course.academic_startyear)
        self.assertEqual(content_json["description"], course.description)
