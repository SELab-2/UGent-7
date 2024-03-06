from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views.user_view import UserViewSet
from api.views.teacher_view import TeacherViewSet
from api.views.admin_view import AdminViewSet
from api.views.assistant_view import AssistantViewSet
from api.views.student_view import StudentViewSet
from api.views.project_view import ProjectViewSet
from api.views.group_view import GroupViewSet
from api.views.course_view import CourseViewSet
from api.views.submission_view import SubmissionViewSet
from api.views.faculty_view import FacultyViewSet
from api.views.checks_view import (
    ExtraCheckViewSet, FileExtensionViewSet, StructureCheckViewSet
)


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"teachers", TeacherViewSet, basename="teacher")
router.register(r"admins", AdminViewSet, basename="admin")
router.register(r"assistants", AssistantViewSet, basename="assistant")
router.register(r"students", StudentViewSet, basename="student")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"submissions", SubmissionViewSet, basename="submission")
router.register(r"structure_checks", StructureCheckViewSet, basename="structure_check")
router.register(r"extra_checks", ExtraCheckViewSet, basename="extra_check")
router.register(r"fileExtensions", FileExtensionViewSet, basename="fileExtension")
router.register(r"faculties", FacultyViewSet, basename="faculty")

urlpatterns = [
    path("", include(router.urls)),
]
