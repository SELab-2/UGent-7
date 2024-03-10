from typing import Tuple

from authentication.cas.client import client
from authentication.models import User
from authentication.signals import user_created, user_login
from django.contrib.auth import login
from django.contrib.auth.models import update_last_login
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedRelatedField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class CASTokenObtainSerializer(Serializer):
    """Serializer for CAS ticket validation
    This serializer takes the CAS ticket and tries to validate it.
    Upon successful validation, create a new user if it doesn't exist.
    """

    ticket = CharField(required=True, min_length=49, max_length=49)

    def validate(self, data):
        """Validate a ticket using CAS client"""
        # Validate the ticket and get CAS attributes.
        attributes = self._validate_ticket(data["ticket"])

        # Fetch a user model from the CAS attributes.
        user, created = self._fetch_user_from_cas(attributes)

        # Update the user's last login.
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(self, user)

        # Login and send authentication signals.
        if "request" in self.context:
            login(self.context["request"], user)

        user_login.send(sender=self, user=user)

        if created:
            user_created.send(sender=self, attributes=attributes, user=user)

        # Return access tokens for the now logged-in user.
        return {
            "access": str(AccessToken.for_user(user)),
            "refresh": str(RefreshToken.for_user(user)),
        }

    def _validate_ticket(self, ticket: str) -> dict:
        """Validate a CAS ticket using the CAS client"""
        response = client.perform_service_validate(ticket=ticket)

        if response.error:
            raise ValidationError(response.error)

        return response.data.get("attributes", dict)

    def _fetch_user_from_cas(self, attributes: dict) -> Tuple[User, bool]:
        if attributes.get("lastenrolled"):
            attributes["lastenrolled"] = int(attributes.get("lastenrolled").split()[0])

        user = UserSerializer(
            data={
                "id": attributes.get("ugentID"),
                "username": attributes.get("uid"),
                "email": attributes.get("mail"),
                "first_name": attributes.get("givenname"),
                "last_name": attributes.get("surname"),
                "last_enrolled": attributes.get("lastenrolled"),
            }
        )

        if not user.is_valid():
            raise ValidationError(user.errors)

        return user.get_or_create(user.validated_data)


class UserSerializer(ModelSerializer):
    """Serializer for the user model
    This serializer validates the user fields for creation and updating.
    """

    id = CharField()
    username = CharField()
    email = EmailField()

    faculties = HyperlinkedRelatedField(
        many=True, read_only=True, view_name="faculty-detail"
    )

    notifications = HyperlinkedRelatedField(
        view_name="notification-detail",
        read_only=True,
    )

    class Meta:
        model = User
        fields = "__all__"

    def get_or_create(self, validated_data: dict) -> Tuple[User, bool]:
        """Create or fetch the user based on the validated data."""
        return User.objects.get_or_create(**validated_data)
