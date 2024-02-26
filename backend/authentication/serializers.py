from rest_framework.serializers import CharField, EmailField, ModelSerializer, DateTimeField, ValidationError, Serializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from authentication.services import users
from authentication.models import User
from authentication.cas.client import client

class CASTokenObtainSerializer(Serializer):
    """Serializer for CAS ticket validation
    This serializer takes the CAS ticket and tries to validate it.
    Upon successful validation, create a new user if it doesn't exist.
    """
    token = RefreshToken
    ticket = CharField(required=True, min_length=49, max_length=49)

    def validate(self, data):
        """Validate a ticket using CAS client"""
        response = client.perform_service_validate(
            ticket=data['ticket']
        )

        if response.error:
            raise ValidationError(response.error)

        # Validation success: create user if it doesn't exist yet.
        attributes = response.data.get('attributes', dict)

        user = users.get_or_create(
            user_id = attributes.get('ugentID'),
            student_id = attributes.get('ugentStudentID'),
            username = attributes.get('uid'),
            email = attributes.get('mail'),
            first_name = attributes.get('givenname'),
            last_name = attributes.get('surname'),
            faculty = attributes.get('faculty'),
            last_enrolled = attributes.get('lastenrolled')
        )

        return {
            'access': str(AccessToken.for_user(user)),
            'refresh': str(RefreshToken.for_user(user))
        }

class UserSerializer(ModelSerializer):
    """Serializer for the user model
    This serializer validates the user fields for creation and updating.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'student_id', 'email',
            'first_name', 'last_name',
            'faculty',
            'last_enrolled', 'last_login', 'create_time'
        ]