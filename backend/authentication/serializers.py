from rest_framework.serializers import Serializer, CharField, EmailField, ModelSerializer, DateTimeField, ValidationError
from authentication.models import User
from authentication.cas.client import client

class CASTicketSerializer(Serializer):
    """Serializer for CAS ticket validation
    This serializer takes the CAS ticket and tries to validate it.
    Upon successful validation, the user field will contain a UserSerializer.
    """
    ticket = CharField(required=True, min_length=49, max_length=49)

    def validate(self, data: dict) -> dict:
        """Validate a ticket using CAS client"""
        response = client.perform_service_validate(
            ticket=data['ticket']
        )

        if response.error:
            raise ValidationError(response.error)

        attributes = response.data.get('attributes', dict)

        # Convert the CAS attributes to a user object.
        user = UserSerializer(data={
            'id': attributes.get('ugentID'),
            'username': attributes.get('uid'),
            'student_id': attributes.get('ugentStudentID'),
            'faculty': attributes.get('faculty'),
            'email': attributes.get('mail'),
            'first_name': attributes.get('givenname'),
            'last_name': attributes.get('surname'),
            'last_enrolled': attributes.get('lastenrolled')
        })

        if not user.is_valid():
            raise ValidationError(user.errors)

        data['user'] = user.validated_data

        return data

class UserSerializer(ModelSerializer):
    """Serializer for the user model
    This serializer validates the user fields for creation and updating.
    """
    id = CharField()
    username = CharField()
    student_id = CharField(allow_null=True)
    faculty = CharField(allow_null=True)
    email = EmailField()
    first_name = CharField()
    last_name = CharField()
    create_time = DateTimeField(required=False)
    last_enrolled = CharField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'student_id', 'email',
            'first_name', 'last_name',
            'faculty',
            'last_enrolled', 'last_login', 'create_time'
        ]