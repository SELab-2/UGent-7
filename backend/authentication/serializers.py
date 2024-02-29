from django.contrib.auth.models import update_last_login
from rest_framework.serializers import CharField, EmailField, ModelSerializer, ValidationError, Serializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.settings import api_settings
from authentication.signals import user_created, user_login
from authentication.models import User
from authentication.cas.client import client

class CASTokenObtainSerializer(Serializer):
    """Serializer for CAS ticket validation
    This serializer takes the CAS ticket and tries to validate it.
    Upon successful validation, create a new user if it doesn't exist.

    /auth/token
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

        if attributes.get('lastenrolled'):
            attributes['lastenrolled'] = int(attributes.get('lastenrolled').split()[0])

        user = UserSerializer(data={
            'id': attributes.get('ugentID'),
            'username': attributes.get('uid'),
            'email': attributes.get('mail'),
            'first_name': attributes.get('givenname'),
            'last_name': attributes.get('surname'),
            'last_enrolled': attributes.get('lastenrolled')
        })

        if not user.is_valid():
            raise ValidationError(user.errors)

        user, created = user.get_or_create(
            user.validated_data
        )

        # Update the user's last login.
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(self, user)

        user_login.send(sender=self,
            user=user
        )

        # Send signal upon creation.
        if created:
            user_created.send(sender=self,
                attributes=attributes,
                user=user
            )

        return {
            'access': str(AccessToken.for_user(user)),
            'refresh': str(RefreshToken.for_user(user))
        }

class UserSerializer(ModelSerializer):
    """Serializer for the user model
    This serializer validates the user fields for creation and updating.
    """
    id = CharField()
    username = CharField()
    email = EmailField()
  
    class Meta:
        model = User
        fields = '__all__'

    def get_or_create(self, validated_data: dict) -> User:
        """Create or fetch the user based on the validated data."""
        return User.objects.get_or_create(**validated_data)