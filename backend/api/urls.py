from django.urls import include, path
from api.views import teacher_view
from api.views import admin_view
from api.views import assistant_view
from api.views import student_view
from api.views import project_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'teachers', Teacher_view)
router.register(r'teachers', teacher_view.TeacherViewSet, basename='teacher')
router.register(r'admins', admin_view.AdminViewSet, basename='admin')
router.register(r'assistants', assistant_view.AssistantViewSet, basename='assistant')
router.register(r'students', student_view.StudentViewSet, basename='student')
router.register(r'projects', project_view.ProjectViewSet, basename='project')

urlpatterns = [
	path('', include(router.urls)),
]
