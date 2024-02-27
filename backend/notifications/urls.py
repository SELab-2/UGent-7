from django.urls import path
from notifications import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.NotificationList.as_view()),
    path("<int:pk>/", views.NotificationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
