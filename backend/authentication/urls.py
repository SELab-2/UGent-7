from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from authentication.views import CASViewSet, TestUser

router = DefaultRouter()
router.register("cas", CASViewSet, "cas")
router.register("test-user", TestUser, "test-user")

urlpatterns = [
    # AUTH endpoints.
    path("", include(router.urls)),
    # TOKEN endpoints.
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
