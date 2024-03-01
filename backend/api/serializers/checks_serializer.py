from rest_framework import serializers
from ..models.checks import Checks, FileExtension


class ChecksSerializer(serializers.ModelSerializer):
    allowed_file_extensions = serializers.StringRelatedField(many=True)
    forbidden_file_extensions = serializers.StringRelatedField(many=True)

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
