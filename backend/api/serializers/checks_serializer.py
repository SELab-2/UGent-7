from rest_framework import serializers
from ..models.checks import Checks, FileExtension


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields = ['id', 'dockerfile',
                  'allowed_file_extensions', 'forbidden_file_extensions']


class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = [
         'id', 'extension'
         ]
