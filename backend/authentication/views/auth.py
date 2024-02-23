from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def login(request: HttpRequest) -> JsonResponse:
    raise NotImplementedError()

@require_http_methods(['GET', 'POST'])
def logout(request: HttpRequest) -> JsonResponse:
    raise NotImplementedError()
