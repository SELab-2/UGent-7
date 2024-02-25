from django.urls import include, path
from api.views import Teacher_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'teachers', Teacher_view)
router.register(r'teachers', Teacher_view, basename='teacher')

urlpatterns = [
	path('api/', include((router.urls, 'api'), namespace='api')),
]