import os
import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from api.helpers.check_folder_structure import check_zip_file, parse_zip_file
from api.models.checks import StructureCheck
from api.models.extension import FileExtension
from api.models.course import Course
from api.models.project import Project
from authentication.models import User
from django.conf import settings


def create_course(id, name, academic_startyear):
    """
    Create a Course with the given arguments.
    """
    return Course.objects.create(
        id=id, name=name, academic_startyear=academic_startyear
    )


def create_file_extension(extension):
    """
    Create a FileExtension with the given arguments.
    """
    return FileExtension.objects.create(extension=extension)


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


def create_structure_check(name, project, obligated, blocked):
    """
    Create a StructureCheck with the given arguments.
    """
    structure_check = StructureCheck.objects.create(
        name=name,
        project=project,
    )
    for ch in obligated:
        structure_check.obligated_extensions.add(ch)
    for ch in blocked:
        structure_check.blocked_extensions.add(ch)

    return structure_check


class FileTestsTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(
            User.get_dummy_admin()
        )
        # Set up a temporary directory for MEDIA_ROOT during tests
        self.old_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.normpath(os.path.join(settings.MEDIA_ROOT, '../testing'))

    def tearDown(self):
        # Restore the original MEDIA_ROOT after tests
        settings.MEDIA_ROOT = self.old_media_root

    def test_parsing(self):
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )
        parse_zip_file(project=project, dir_path="structures/zip_struct1.zip")

        response = self.client.get(
            reverse("project-detail", args=[str(project.id)]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        response = self.client.get(
            content_json["structure_checks"], follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 7)

        expected_project_url = settings.TESTING_BASE_LINK + reverse(
            "project-detail", args=[str(project.id)]
        )

        content = content_json[0]
        self.assertEqual(content["name"], ".")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 0)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[1]
        self.assertEqual(content["name"], "folder_struct1")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 1)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[2]
        self.assertEqual(content["name"], "folder_struct1/submap1")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 2)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[3]
        self.assertEqual(content["name"], "folder_struct1/submap1/templates")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 1)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[4]
        self.assertEqual(content["name"], "folder_struct1/submap2")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 1)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[5]
        self.assertEqual(content["name"], "folder_struct1/submap2/src")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 3)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[6]
        self.assertEqual(content["name"], "folder_struct1/submap3")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 2)
        self.assertEqual(len(content["blocked_extensions"]), 0)

    def test_checking(self):
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )

        fileExtensionHS = create_file_extension(extension="hs")
        fileExtensionPDF = create_file_extension(extension="pdf")
        fileExtensionDOCX = create_file_extension(extension="docx")
        fileExtensionLATEX = create_file_extension(extension="latex")
        fileExtensionMD = create_file_extension(extension="md")
        fileExtensionPY = create_file_extension(extension="py")
        fileExtensionHPP = create_file_extension(extension="hpp")
        fileExtensionCPP = create_file_extension(extension="cpp")
        fileExtensionTS = create_file_extension(extension="ts")
        fileExtensionTSX = create_file_extension(extension="tsx")

        create_structure_check(
            name=".",
            project=project,
            obligated=[],
            blocked=[])

        create_structure_check(
            name="folder_struct1",
            project=project,
            obligated=[fileExtensionHS],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1",
            project=project,
            obligated=[fileExtensionPDF, fileExtensionDOCX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1/templates",
            project=project,
            obligated=[fileExtensionLATEX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2",
            project=project,
            obligated=[fileExtensionMD],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2/src",
            project=project,
            obligated=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap3",
            project=project,
            obligated=[fileExtensionTS, fileExtensionTSX],
            blocked=[])

        self.assertTrue(check_zip_file(project=project, dir_path="structures/zip_struct1.zip")[0])

    def test_checking_obligated_not_found(self):
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )

        fileExtensionHS = create_file_extension(extension="hs")
        fileExtensionPDF = create_file_extension(extension="pdf")
        fileExtensionDOCX = create_file_extension(extension="docx")
        fileExtensionLATEX = create_file_extension(extension="latex")
        fileExtensionMD = create_file_extension(extension="md")
        fileExtensionPY = create_file_extension(extension="py")
        fileExtensionHPP = create_file_extension(extension="hpp")
        fileExtensionCPP = create_file_extension(extension="cpp")
        fileExtensionTS = create_file_extension(extension="ts")
        fileExtensionTSX = create_file_extension(extension="tsx")

        create_structure_check(
            name=".",
            project=project,
            obligated=[],
            blocked=[fileExtensionDOCX])

        create_structure_check(
            name="folder_struct1",
            project=project,
            obligated=[fileExtensionHS],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1",
            project=project,
            obligated=[fileExtensionPDF, fileExtensionDOCX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1/templates",
            project=project,
            obligated=[fileExtensionLATEX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2",
            project=project,
            obligated=[fileExtensionMD],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2/src",
            project=project,
            obligated=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap3",
            project=project,
            obligated=[fileExtensionTS, fileExtensionTSX],
            blocked=[])
        self.assertFalse(check_zip_file(project=project, dir_path="tests/test_zip2struct1.zip")[0])

    def test_checking_obligated_directory_not_found(self):
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )

        fileExtensionHS = create_file_extension(extension="hs")
        fileExtensionPDF = create_file_extension(extension="pdf")
        fileExtensionDOCX = create_file_extension(extension="docx")
        fileExtensionLATEX = create_file_extension(extension="latex")
        fileExtensionMD = create_file_extension(extension="md")
        fileExtensionPY = create_file_extension(extension="py")
        fileExtensionHPP = create_file_extension(extension="hpp")
        fileExtensionCPP = create_file_extension(extension="cpp")
        fileExtensionTS = create_file_extension(extension="ts")
        fileExtensionTSX = create_file_extension(extension="tsx")

        create_structure_check(
            name=".",
            project=project,
            obligated=[],
            blocked=[fileExtensionDOCX])

        create_structure_check(
            name="folder_struct1",
            project=project,
            obligated=[fileExtensionHS],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1",
            project=project,
            obligated=[fileExtensionPDF, fileExtensionDOCX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1/templates",
            project=project,
            obligated=[fileExtensionLATEX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2",
            project=project,
            obligated=[fileExtensionMD],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2/src",
            project=project,
            obligated=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap3",
            project=project,
            obligated=[fileExtensionTS, fileExtensionTSX],
            blocked=[])
        self.assertFalse(check_zip_file(project=project, dir_path="tests/test_zip4struct1.zip")[0])

    def test_checking_blocked_extension_found(self):
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )

        fileExtensionHS = create_file_extension(extension="hs")
        fileExtensionPDF = create_file_extension(extension="pdf")
        fileExtensionDOCX = create_file_extension(extension="docx")
        fileExtensionLATEX = create_file_extension(extension="latex")
        fileExtensionMD = create_file_extension(extension="md")
        fileExtensionPY = create_file_extension(extension="py")
        fileExtensionHPP = create_file_extension(extension="hpp")
        fileExtensionCPP = create_file_extension(extension="cpp")
        fileExtensionTS = create_file_extension(extension="ts")
        fileExtensionTSX = create_file_extension(extension="tsx")

        create_structure_check(
            name=".",
            project=project,
            obligated=[],
            blocked=[fileExtensionDOCX])

        create_structure_check(
            name="folder_struct1",
            project=project,
            obligated=[fileExtensionHS],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1",
            project=project,
            obligated=[fileExtensionDOCX],
            blocked=[fileExtensionPDF])

        create_structure_check(
            name="folder_struct1/submap1/templates",
            project=project,
            obligated=[fileExtensionLATEX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2",
            project=project,
            obligated=[fileExtensionMD],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2/src",
            project=project,
            obligated=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap3",
            project=project,
            obligated=[fileExtensionTS, fileExtensionTSX],
            blocked=[])

        self.assertFalse(check_zip_file(project=project, dir_path="tests/test_zip1struct1.zip")[0])

    def test_checking_extra_directory_found(self):
        course = create_course(id=3, name="test course", academic_startyear=2024)
        project = create_project(
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )

        fileExtensionHS = create_file_extension(extension="hs")
        fileExtensionPDF = create_file_extension(extension="pdf")
        fileExtensionDOCX = create_file_extension(extension="docx")
        fileExtensionLATEX = create_file_extension(extension="latex")
        fileExtensionMD = create_file_extension(extension="md")
        fileExtensionPY = create_file_extension(extension="py")
        fileExtensionHPP = create_file_extension(extension="hpp")
        fileExtensionCPP = create_file_extension(extension="cpp")
        fileExtensionTS = create_file_extension(extension="ts")
        fileExtensionTSX = create_file_extension(extension="tsx")

        create_structure_check(
            name=".",
            project=project,
            obligated=[],
            blocked=[fileExtensionDOCX])

        create_structure_check(
            name="folder_struct1",
            project=project,
            obligated=[fileExtensionHS],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1",
            project=project,
            obligated=[fileExtensionPDF, fileExtensionDOCX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap1/templates",
            project=project,
            obligated=[fileExtensionLATEX],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2",
            project=project,
            obligated=[fileExtensionMD],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap2/src",
            project=project,
            obligated=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
            blocked=[])

        create_structure_check(
            name="folder_struct1/submap3",
            project=project,
            obligated=[fileExtensionTS, fileExtensionTSX],
            blocked=[])

        self.assertFalse(
            check_zip_file(project=project, dir_path="tests/test_zip3struct1.zip", restrict_extra_folders=True)[0])
