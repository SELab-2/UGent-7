from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from authentication.views.auth import WhoAmIView, LoginView, LogoutView, TokenEchoView
from authentication.views.users import UsersView

router = DefaultRouter()
router.register("users", UsersView, basename="user")

urlpatterns = [
    # USER endpoints.
    path("", include(router.urls)),
    # AUTH endpoints.
    path("login", LoginView.as_view(), name="auth.login"),
    path("logout", LogoutView.as_view(), name="auth.logout"),
    path("whoami", WhoAmIView.as_view(), name="auth.whoami"),
    path("echo", TokenEchoView.as_view(), name="auth.echo"),
    # TOKEN endpoints.
    path("token", TokenObtainPairView.as_view(), name="auth.token"),
    path("token/refresh", TokenRefreshView.as_view(), name="auth.token.refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="auth.token.verify"),
]
