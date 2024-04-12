from django.db.models import Min, Max
from rest_framework.response import Response
from api.models.course import Course
from api.views.pagination.basic_pagination import BasicPagination


class CoursePagination(BasicPagination):
    def get_paginated_response(self, schema):
        # Get min and max years
        years = Course.objects.all().aggregate(
            Min('academic_startyear'), Max('academic_startyear')
        )

        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'min_year': years['academic_startyear__min'],
            'max_year': years['academic_startyear__max'],
            'results': schema,
        })
