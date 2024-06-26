"""
URL configuration for ypovoli project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.http import JsonResponse
from ypovoli.settings import DOMAIN_NAME

schema_view = get_schema_view(
    openapi.Info(
        title="Ypovoli API",
        default_version="v1.0.0",
        description="API used for the Ypovoli application.",
        license=openapi.License(name="MIT License"),
        contact=openapi.Contact(email="Tybo.Verslype@ugent.be"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    url=f"https://{DOMAIN_NAME}",
)


def swagger_json(request):
    """Return the Swagger JSON content."""
    schema = schema_view.without_ui(cache_timeout=0)(request)
    return JsonResponse(schema.data)


urlpatterns = [
    path(
        "api/",
        include(
            [
                path("", swagger_json, name="swagger-json"),
                # Base API endpoints.
                path("", include("api.urls")),
                # Authentication endpoints.
                path("auth/", include("authentication.urls")),
                # Swagger documentation.
                path(
                    "swagger/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
                path(
                    "swagger<format>/",
                    schema_view.without_ui(cache_timeout=0),
                    name="schema-json",
                ),
            ]
        ),
    )
]
