from django.urls import include, path
from api.views import teacher_view
from api.views import admin_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'teachers', Teacher_view)
router.register(r'teachers', teacher_view.TeacherViewSet, basename='teacher')
router.register(r'admins', admin_view.AdminViewSet, basename='admin')

urlpatterns = [
	path('', include(router.urls)),
]
