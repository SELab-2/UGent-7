from django.urls import include, path
from api.views import Teacher_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'teachers', Teacher_view)
router.register(r'teachers', Teacher_view.TeacherViewSet, basename='teacher')

urlpatterns = [
	path('', include(router.urls)),
]
