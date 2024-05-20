from typing import Type

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import Serializer


class ExpandableHyperlinkedIdentityField(serializers.BaseSerializer, serializers.HyperlinkedIdentityField):
    """A HyperlinkedIdentityField with nested serializer expanding"""
    def __init__(self, serializer: Type[Serializer], view_name: str = None, **kwargs):
        self.serializer = serializer
        super().__init__(view_name=view_name, **kwargs)

    def get_url(self, obj: any, view_name: str, request: Request, fm: str):
        """Get the URL of the related object"""
        return super().get_url(obj, view_name, request, fm)

    def to_representation(self, value):
        """Get the representation of the nested instance"""
        request: Request = self.context.get('request')

        if request and self.field_name in request.query_params:
            try:
                instance = getattr(value, self.field_name)
            except AttributeError:
                instance = value

            return self.serializer(instance,
                many=self._kwargs.pop('many'),
                context=self.context
            ).data

        return super(serializers.HyperlinkedIdentityField, self).to_representation(value)
