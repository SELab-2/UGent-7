from rest_framework.response import Response
from api.views.pagination.basic_pagination import BasicPagination


class UserPagination(BasicPagination):
    def get_paginated_response(self, schema):

        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': schema,
        })
