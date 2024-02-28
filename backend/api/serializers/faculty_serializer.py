from rest_framework import serializers
from authentication.models import Faculty


class facultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            'name'
          ]
