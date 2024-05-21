from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from authentication.models import Faculty


class FacultySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, data) -> str:
        return _(data.name)

    class Meta:
        model = Faculty
        fields = ["id", "name"]
