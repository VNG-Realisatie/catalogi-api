from collections import OrderedDict

from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param


class HALPagination(PageNumberPagination):
    page_query_param = settings.REST_FRAMEWORK_EXT.get('PAGE_PARAM', 'page')

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        return remove_query_param(url, self.page_query_param)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, self.page.paginator.num_pages)

    def get_paginated_response(self, data):
        def link(url, description=None):
            data = [('href', url), ]
            if description:
                data.append(('desc', description))
            return OrderedDict(data)

        links_data = [
            ('self', link(self.request.build_absolute_uri())),
        ]

        if self.page.number > 1:
            links_data.extend([
                ('first', link(self.get_first_link())),
                ('prev', link(self.get_previous_link())),
            ])
        if self.page.number < self.page.paginator.num_pages:
            links_data.append(
                ('next', link(self.get_next_link())),
            )
        if self.page.paginator.num_pages > 1:
            links_data.append(
                ('last', link(self.get_last_link())),
            )

        return Response(OrderedDict([
            ('_links', OrderedDict(links_data)),
            ('results', data)
        ]), headers={
            'X-Total-Count': self.page.paginator.count,
            'X-Pagination-Count': self.page.paginator.num_pages,
            'X-Pagination-Page': self.page.number,
            'X-Pagination-Limit': self.get_page_size(self.request),
        })
