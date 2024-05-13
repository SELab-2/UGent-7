import json
import os

from api.logic.parse_zip_files import parse_zip
from api.tests.helpers import create_course, create_project
from authentication.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase


class FileTestsTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(  # type: ignore
            User.get_dummy_admin()
        )
        # Set up a temporary directory for MEDIA_ROOT during tests
        self.old_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.normpath(os.path.join(settings.MEDIA_ROOT, '../testing'))

    def tearDown(self):
        # Restore the original MEDIA_ROOT after tests
        settings.MEDIA_ROOT = self.old_media_root

    def test_parsing(self):
        course = create_course(name="test course", academic_startyear=2024)
        project = create_project(
            group_size=5,
            max_score=10,
            name="test",
            description="descr",
            visible=True,
            archived=False,
            days=100,
            course=course,
        )

        memory_file = SimpleUploadedFile("zip_struct1.zip", open(
            f"{settings.MEDIA_ROOT}/structures/zip_struct1.zip", "rb").read(), content_type='application/zip')

        parse_zip(project=project, zip_file=memory_file)

        response = self.client.get(
            reverse("project-structure-checks", args=[str(project.id)]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, "application/json")  # type: ignore

        content_json = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content_json), 6)

        expected_project_url = settings.TESTING_BASE_LINK + reverse(
            "project-detail", args=[str(project.id)]
        )

        content = content_json[0]
        self.assertEqual(content["path"], "folder_struct1/submap1/")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 2)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[1]
        self.assertEqual(content["path"], "folder_struct1/submap1/templates/")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 1)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[2]
        self.assertEqual(content["path"], "folder_struct1/submap2/")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 1)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[3]
        self.assertEqual(content["path"], "folder_struct1/submap2/src/")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 3)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[4]
        self.assertEqual(content["path"], "folder_struct1/submap3/")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 2)
        self.assertEqual(len(content["blocked_extensions"]), 0)

        content = content_json[5]
        self.assertEqual(content["path"], "folder_struct1/")
        self.assertEqual(content["project"], expected_project_url)
        self.assertEqual(len(content["obligated_extensions"]), 1)
        self.assertEqual(len(content["blocked_extensions"]), 0)

    # def test_checking(self):
    #     course = create_course(name="test course", academic_startyear=2024)
    #     project = create_project(
    #         max_score=10,
    #         group_size=5,
    #         name="test",
    #         description="descr",
    #         visible=True,
    #         archived=False,
    #         days=100,
    #         course=course,
    #     )

    #     fileExtensionHS = create_file_extension(extension="hs")
    #     fileExtensionPDF = create_file_extension(extension="pdf")
    #     fileExtensionDOCX = create_file_extension(extension="docx")
    #     fileExtensionLATEX = create_file_extension(extension="latex")
    #     fileExtensionMD = create_file_extension(extension="md")
    #     fileExtensionPY = create_file_extension(extension="py")
    #     fileExtensionHPP = create_file_extension(extension="hpp")
    #     fileExtensionCPP = create_file_extension(extension="cpp")
    #     fileExtensionTS = create_file_extension(extension="ts")
    #     fileExtensionTSX = create_file_extension(extension="tsx")

    #     create_structure_check(
    #         path="",
    #         project=project,
    #         obligated_extensions=[],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/",
    #         project=project,
    #         obligated_extensions=[fileExtensionHS],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1/",
    #         project=project,
    #         obligated_extensions=[fileExtensionPDF, fileExtensionDOCX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1/templates/",
    #         project=project,
    #         obligated_extensions=[fileExtensionLATEX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2/",
    #         project=project,
    #         obligated_extensions=[fileExtensionMD],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2/src/",
    #         project=project,
    #         obligated_extensions=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap3/",
    #         project=project,
    #         obligated_extensions=[fileExtensionTS, fileExtensionTSX],
    #         blocked_extensions=[])

    #     self.assertTrue(check_zip_file(project=project, dir_path="structures/zip_struct1.zip")[0])

    # def test_checking_obligated_not_found(self):
    #     course = create_course(name="test course", academic_startyear=2024)
    #     project = create_project(
    #         group_size=5,
    #         max_score=10,
    #         name="test",
    #         description="descr",
    #         visible=True,
    #         archived=False,
    #         days=100,
    #         course=course,
    #     )

    #     fileExtensionHS = create_file_extension(extension="hs")
    #     fileExtensionPDF = create_file_extension(extension="pdf")
    #     fileExtensionDOCX = create_file_extension(extension="docx")
    #     fileExtensionLATEX = create_file_extension(extension="latex")
    #     fileExtensionMD = create_file_extension(extension="md")
    #     fileExtensionPY = create_file_extension(extension="py")
    #     fileExtensionHPP = create_file_extension(extension="hpp")
    #     fileExtensionCPP = create_file_extension(extension="cpp")
    #     fileExtensionTS = create_file_extension(extension="ts")
    #     fileExtensionTSX = create_file_extension(extension="tsx")

    #     create_structure_check(
    #         path=".",
    #         project=project,
    #         obligated_extensions=[],
    #         blocked_extensions=[fileExtensionDOCX])

    #     create_structure_check(
    #         path="folder_struct1",
    #         project=project,
    #         obligated_extensions=[fileExtensionHS],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1",
    #         project=project,
    #         obligated_extensions=[fileExtensionPDF, fileExtensionDOCX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1/templates",
    #         project=project,
    #         obligated_extensions=[fileExtensionLATEX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2",
    #         project=project,
    #         obligated_extensions=[fileExtensionMD],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2/src",
    #         project=project,
    #         obligated_extensions=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap3",
    #         project=project,
    #         obligated_extensions=[fileExtensionTS, fileExtensionTSX],
    #         blocked_extensions=[])
    #     self.assertFalse(check_zip_file(project=project, dir_path="tests/test_zip2struct1.zip")[0])

    # def test_checking_obligated_directory_not_found(self):
    #     course = create_course(name="test course", academic_startyear=2024)
    #     project = create_project(
    #         group_size=5,
    #         max_score=10,
    #         name="test",
    #         description="descr",
    #         visible=True,
    #         archived=False,
    #         days=100,
    #         course=course,
    #     )

    #     fileExtensionHS = create_file_extension(extension="hs")
    #     fileExtensionPDF = create_file_extension(extension="pdf")
    #     fileExtensionDOCX = create_file_extension(extension="docx")
    #     fileExtensionLATEX = create_file_extension(extension="latex")
    #     fileExtensionMD = create_file_extension(extension="md")
    #     fileExtensionPY = create_file_extension(extension="py")
    #     fileExtensionHPP = create_file_extension(extension="hpp")
    #     fileExtensionCPP = create_file_extension(extension="cpp")
    #     fileExtensionTS = create_file_extension(extension="ts")
    #     fileExtensionTSX = create_file_extension(extension="tsx")

    #     create_structure_check(
    #         path=".",
    #         project=project,
    #         obligated_extensions=[],
    #         blocked_extensions=[fileExtensionDOCX])

    #     create_structure_check(
    #         path="folder_struct1",
    #         project=project,
    #         obligated_extensions=[fileExtensionHS],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1",
    #         project=project,
    #         obligated_extensions=[fileExtensionPDF, fileExtensionDOCX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1/templates",
    #         project=project,
    #         obligated_extensions=[fileExtensionLATEX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2",
    #         project=project,
    #         obligated_extensions=[fileExtensionMD],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2/src",
    #         project=project,
    #         obligated_extensions=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap3",
    #         project=project,
    #         obligated_extensions=[fileExtensionTS, fileExtensionTSX],
    #         blocked_extensions=[])
    #     self.assertFalse(check_zip_file(project=project, dir_path="tests/test_zip4struct1.zip")[0])

    # def test_checking_blocked_extension_found(self):
    #     course = create_course(name="test course", academic_startyear=2024)
    #     project = create_project(
    #         group_size=5,
    #         max_score=10,
    #         name="test",
    #         description="descr",
    #         visible=True,
    #         archived=False,
    #         days=100,
    #         course=course,
    #     )

    #     fileExtensionHS = create_file_extension(extension="hs")
    #     fileExtensionPDF = create_file_extension(extension="pdf")
    #     fileExtensionDOCX = create_file_extension(extension="docx")
    #     fileExtensionLATEX = create_file_extension(extension="latex")
    #     fileExtensionMD = create_file_extension(extension="md")
    #     fileExtensionPY = create_file_extension(extension="py")
    #     fileExtensionHPP = create_file_extension(extension="hpp")
    #     fileExtensionCPP = create_file_extension(extension="cpp")
    #     fileExtensionTS = create_file_extension(extension="ts")
    #     fileExtensionTSX = create_file_extension(extension="tsx")

    #     create_structure_check(
    #         path=".",
    #         project=project,
    #         obligated_extensions=[],
    #         blocked_extensions=[fileExtensionDOCX])

    #     create_structure_check(
    #         path="folder_struct1",
    #         project=project,
    #         obligated_extensions=[fileExtensionHS],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1",
    #         project=project,
    #         obligated_extensions=[fileExtensionDOCX],
    #         blocked_extensions=[fileExtensionPDF])

    #     create_structure_check(
    #         path="folder_struct1/submap1/templates",
    #         project=project,
    #         obligated_extensions=[fileExtensionLATEX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2",
    #         project=project,
    #         obligated_extensions=[fileExtensionMD],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2/src",
    #         project=project,
    #         obligated_extensions=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap3",
    #         project=project,
    #         obligated_extensions=[fileExtensionTS, fileExtensionTSX],
    #         blocked_extensions=[])

    #     self.assertFalse(check_zip_file(project=project, dir_path="tests/test_zip1struct1.zip")[0])

    # def test_checking_extra_directory_found(self):
    #     course = create_course(name="test course", academic_startyear=2024)
    #     project = create_project(
    #         group_size=5,
    #         max_score=10,
    #         name="test",
    #         description="descr",
    #         visible=True,
    #         archived=False,
    #         days=100,
    #         course=course,
    #     )

    #     fileExtensionHS = create_file_extension(extension="hs")
    #     fileExtensionPDF = create_file_extension(extension="pdf")
    #     fileExtensionDOCX = create_file_extension(extension="docx")
    #     fileExtensionLATEX = create_file_extension(extension="latex")
    #     fileExtensionMD = create_file_extension(extension="md")
    #     fileExtensionPY = create_file_extension(extension="py")
    #     fileExtensionHPP = create_file_extension(extension="hpp")
    #     fileExtensionCPP = create_file_extension(extension="cpp")
    #     fileExtensionTS = create_file_extension(extension="ts")
    #     fileExtensionTSX = create_file_extension(extension="tsx")

    #     create_structure_check(
    #         path=".",
    #         project=project,
    #         obligated_extensions=[],
    #         blocked_extensions=[fileExtensionDOCX])

    #     create_structure_check(
    #         path="folder_struct1",
    #         project=project,
    #         obligated_extensions=[fileExtensionHS],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1",
    #         project=project,
    #         obligated_extensions=[fileExtensionPDF, fileExtensionDOCX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap1/templates",
    #         project=project,
    #         obligated_extensions=[fileExtensionLATEX],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2",
    #         project=project,
    #         obligated_extensions=[fileExtensionMD],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap2/src",
    #         project=project,
    #         obligated_extensions=[fileExtensionPY, fileExtensionHPP, fileExtensionCPP],
    #         blocked_extensions=[])

    #     create_structure_check(
    #         path="folder_struct1/submap3",
    #         project=project,
    #         obligated_extensions=[fileExtensionTS, fileExtensionTSX],
    #         blocked_extensions=[])

    #     self.assertFalse(
    #         check_zip_file(project=project, dir_path="tests/test_zip3struct1.zip", restrict_extra_folders=True)[0])
