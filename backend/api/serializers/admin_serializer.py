from rest_framework import serializers
from ..models.admin import Admin


class AdminSerializer(serializers.ModelSerializer):

    faculties = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='faculty-detail'
    )

    class Meta:
        model = Admin
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'faculties', 'last_enrolled', 'create_time'
          ]
