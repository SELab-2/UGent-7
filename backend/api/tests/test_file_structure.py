import os
import tempfile
from django.test import TestCase
from django.core.files.base import ContentFile
from api.views.check_folder_structure import check_zip_content, parseZipFile
from api.models.checks import StructureCheck
from api.models.project import Project
from django.conf import settings


class FileTestsTests(TestCase):
    def setUp(self):
        # Set up a temporary directory for MEDIA_ROOT during tests
        self.old_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.normpath(os.path.join(settings.MEDIA_ROOT, '../testing'))

    def tearDown(self):
        # Restore the original MEDIA_ROOT after tests
        settings.MEDIA_ROOT = self.old_media_root

    def test_your_function(self):
        # Test your function that interacts with the media directory
        self.assertEqual(True, True)
