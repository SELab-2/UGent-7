from django.urls import include, path
from api.views import teacher_view
from api.views import admin_view
from api.views import assistant_view
from api.views import student_view
from api.views import project_view
from api.views import group_view
from api.views import submision_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'teachers', teacher_view.TeacherViewSet, basename='teacher')
router.register(r'admins', admin_view.AdminViewSet, basename='admin')
router.register(r'assistants', assistant_view.AssistantViewSet, basename='assistant')
router.register(r'students', student_view.StudentViewSet, basename='student')
router.register(r'projects', project_view.ProjectViewSet, basename='project')
router.register(r'groups', group_view.GroupViewSet, basename='group')
router.register(r'submissions', submision_view.SubmissionViewSet, basename='submission')
router.register(r'submission_file', submision_view.SubmissionFileViewSet, basename='submission_file')

urlpatterns = [
	path('', include(router.urls)),
]
