from django.urls import include, path
from api.views import teacher_view
from api.views import admin_view
from api.views import assistant_view
from api.views import student_view
from api.views import project_view
from api.views import group_view
from api.views import course_view
from api.views import submision_view
from api.views import checks_view
from api.views import faculty_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'teachers',
    teacher_view.TeacherViewSet,
    basename='teacher')
router.register(
    r'admins',
    admin_view.AdminViewSet,
    basename='admin')
router.register(
    r'assistants',
    assistant_view.AssistantViewSet,
    basename='assistant')
router.register(
    r'students',
    student_view.StudentViewSet,
    basename='student')
router.register(
    r'projects',
    project_view.ProjectViewSet,
    basename='project')
router.register(
    r'groups',
    group_view.GroupViewSet,
    basename='group')
router.register(
    r'courses',
    course_view.CourseViewSet,
    basename='course')
router.register(
    r'submissions',
    submision_view.SubmissionViewSet,
    basename='submission')
router.register(
    r'checks',
    checks_view.ChecksViewSet,
    basename='check')
router.register(
    r'fileExtensions',
    checks_view.FileExtensionViewSet,
    basename='fileExtension')
router.register(
    r'facultys',
    faculty_view.facultyViewSet,
    basename='faculty')

urlpatterns = [
    path('', include(router.urls)),

    path('assistants/<int:assistant_id>/courses/',
         assistant_view.AssistantCoursesViewSet.as_view({'get': 'list'}),
         name='assistant-courses'),

    path('students/<int:student_id>/courses/',
         student_view.StudentCoursesViewSet.as_view({'get': 'list'}),
         name='student-courses'),
    path('students/<int:student_id>/groups/',
         student_view.StudentGroupsViewSet.as_view({'get': 'list'}),
         name='student-groups'),

    path('teachers/<int:teacher_id>/courses/',
         teacher_view.TeacherCoursesViewSet.as_view({'get': 'list'}),
         name='teacher-courses'),
    
]
