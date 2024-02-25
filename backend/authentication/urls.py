from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from authentication.views import WhoAmIView, LoginView, LogoutView, TokenEchoView

urlpatterns = [
    # CAS endpoints.
    path('login', LoginView.as_view(), name='auth.login'),
    path('logout', LogoutView.as_view(), name='auth.logout'),
    path('whoami', WhoAmIView.as_view(), name='auth.whoami'),
    path('echo', TokenEchoView.as_view(), name='auth.echo'),
    # TOKEN endpoints.
    path('token', TokenObtainPairView.as_view(), name='auth.token'),
    path('token/refresh', TokenRefreshView.as_view(), name='auth.token.refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='auth.token.verify')
]