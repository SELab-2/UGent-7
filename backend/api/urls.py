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

urlpatterns = [
    path('', include(router.urls)),

    path('courses/<int:course_id>/teachers/',
         course_view.CourseTeachersViewSet.as_view({'get': 'list'}),
         name='course-teachers'),
    path('courses/<int:course_id>/assistants/',
         course_view.CourseAssistantsViewSet.as_view({'get': 'list'}),
         name='course-assistants'),
    path('courses/<int:course_id>/students/',
         course_view.CourseStudentsViewSet.as_view({'get': 'list'}),
         name='course-students'),
    path('courses/<int:course_id>/projects/',
         course_view.CourseProjectsViewSet.as_view({'get': 'list'}),
         name='course-projects'),

    path('assistants/<int:assistant_id>/courses/',
         assistant_view.AssistantCoursesViewSet.as_view({'get': 'list'}),
         name='assistant-courses'),

    path('students/<int:student_id>/courses/',
         student_view.StudentCoursesViewSet.as_view({'get': 'list'}),
         name='student-courses'),

    path('teachers/<int:teacher_id>/courses/',
         teacher_view.TeacherCoursesViewSet.as_view({'get': 'list'}),
         name='teacher-courses'),
    
]
