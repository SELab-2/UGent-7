from rest_framework.serializers import Serializer, CharField

class ValidateSerializer(Serializer):
    ticket = CharField(required=True)