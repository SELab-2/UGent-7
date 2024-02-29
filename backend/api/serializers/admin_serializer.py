from rest_framework import serializers
from ..models.admin import Admin


class AdminSerializer(serializers.ModelSerializer):


    class Meta:
        model = Admin
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculties', 'last_enrolled', 'create_time'
          ]
