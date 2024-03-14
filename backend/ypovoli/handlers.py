from rest_framework.views import exception_handler
from django.utils.translation import gettext_lazy as _


def translate_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response.status_code == 401:
        response.data['detail'] = _('Given token not valid for any token type')

    if response.status_code == 404:
        response.data['detail'] = _('Not found.')

    return response
