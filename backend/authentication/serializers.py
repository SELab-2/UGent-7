from rest_framework.serializers import Serializer, CharField

class CASTicketSerializer(Serializer):
    """Serializer for CAS ticket validation"""
    ticket = CharField(required=True, min_length=49, max_length=49)


class CASUserSerializer(Serializer):
    """Serializer for CAS success responses"""

class UserSerializer(Serializer):
    """Serializer for User models"""