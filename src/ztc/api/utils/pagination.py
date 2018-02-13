from collections import OrderedDict

from django.conf import settings

from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class HALPagination(PageNumberPagination):
    page_query_param = settings.REST_FRAMEWORK_EXT.get('PAGE_PARAM', 'page')

    header_total_count = 'X-Total-Count'
    header_pagination_count = 'X-Pagination-Count'
    header_pagination_page = 'X-Pagination-Page'
    header_pagination_limit = 'X-Pagination-Limit'

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
            self.header_total_count: self.page.paginator.count,
            self.header_pagination_count: self.page.paginator.num_pages,
            self.header_pagination_page: self.page.number,
            self.header_pagination_limit: self.get_page_size(self.request),
        })


class HALPaginationInspector(PaginatorInspector):
    """
    Provides response schema pagination warpping for `HALPagination`.

    Hook for `drf-yasg`.
    """
    def get_paginated_response(self, paginator, response_schema):
        assert response_schema.type == openapi.TYPE_ARRAY, "array return expected for paged response"
        paged_schema = None
        if isinstance(paginator, HALPagination):
            paged_schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=OrderedDict((
                    ('_links', openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=OrderedDict((
                            ('self', openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description='URL to the current page in the result set.'
                            )),
                            ('first', openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description='URL to the first page in the result set.',
                            )),
                            ('prev', openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description='URL to the previous page in the result set.',
                            )),
                            ('next', openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description='URL to the next page in the result set.',
                            )),
                            ('last', openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description='URL to the last page in the result set.',
                            )),
                        )),
                        required=['self'],
                        description='Pagination meta data about the result set.'
                    )),
                    ('results', response_schema),
                )),
                required=['_links', 'results'],
            )

        # Typically, you return a `openapi.Schema` instance. However, returning a `openapi.Response` allows us to pass
        # headers to the specification.
        # See: http://drf-yasg.readthedocs.io/en/stable/openapi.html?highlight=header#default-behavior
        return openapi.Response(
            description='',
            schema=paged_schema,
            headers=OrderedDict([
                (HALPagination.header_total_count, {
                    'type': openapi.TYPE_INTEGER, 'description': 'Total number of results.'}),
                (HALPagination.header_pagination_count, {
                    'type': openapi.TYPE_INTEGER, 'description': 'Total number of pages.'}),
                (HALPagination.header_pagination_page, {
                    'type': openapi.TYPE_INTEGER, 'description': 'Current page number.'}),
                (HALPagination.header_pagination_limit, {
                    'type': openapi.TYPE_INTEGER, 'description': 'Number of results per page.'}),
            ]),
        )
        # return paged_schema
