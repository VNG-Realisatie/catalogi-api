import logging
import os

from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import (
    CoreAPICompatInspector, NotHandled, SwaggerAutoSchema
)
from drf_yasg.utils import is_list_view
from drf_yasg.views import get_schema_view
from rest_framework import filters, permissions, status
from rest_framework.settings import api_settings

from .utils.pagination import HALPaginationInspector

logger = logging.getLogger(__name__)


try:
    file_path = os.path.join(settings.BASE_DIR, 'docs', 'api', '_description.md')
    with open(file_path, 'r', encoding='utf-8') as f:
        description = f.read()
except FileNotFoundError as e:
    logger.warning('Could not load API documentation description: %s', e)
    description = None


schema_view = get_schema_view(
    openapi.Info(
        title='Zaaktypecatalogus (ZTC) API documentatie',
        default_version='v{}'.format(api_settings.DEFAULT_VERSION),
        description=description,
        # terms_of_service='',
        contact=openapi.Contact(email='support@maykinmedia.nl'),
        license=openapi.License(name='EUPL 1.2'),
    ),
    #validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    """
    Simple filter inspector to set an appropriate description for filter fields.
    """
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super().get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    param.description = "Filter the returned list by {field_name}.".format(field_name=param.name)
            return result

        return NotHandled


class SearchDescriptionInspector(CoreAPICompatInspector):
    """
    Simple filter inspector to set an appropriate description for search fields.
    """
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, filters.SearchFilter):
            search_fields = getattr(self.view, 'search_fields', [])
            result = super().get_filter_parameters(filter_backend)
            for param in result:
                param.description = "One or more search terms, separated by a space, to search the returned list. " \
                                    "The following fields will be searched: {}.".format(', '.join(search_fields))
            return result

        return NotHandled


class OrderingDescriptionInspector(CoreAPICompatInspector):
    """
    Simple filter inspector to set an appropriate description for ordering fields.
    """
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, filters.OrderingFilter):
            ordering_fields = getattr(self.view, 'ordering_fields', [])
            result = super().get_filter_parameters(filter_backend)
            for param in result:
                param.description = "A field name to sort the returned list, ascending by default. " \
                                    "Prefix with a minus to sort descending. " \
                                    "Valid values: {}.".format(', '.join(ordering_fields))
            return result

        return NotHandled


class AutoSchema(SwaggerAutoSchema):
    field_inspectors = [
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS
    filter_inspectors = [
        DjangoFilterDescriptionInspector,
        SearchDescriptionInspector,
        OrderingDescriptionInspector,
    ] + swagger_settings.DEFAULT_FILTER_INSPECTORS
    paginator_inspectors = [
       HALPaginationInspector,
    ] + swagger_settings.DEFAULT_PAGINATOR_INSPECTORS

    def get_default_responses(self):
        """Get the default responses determined for this view from the request serializer and request method.

        :type: dict[str, openapi.Schema]
        """
        ret = super().get_default_responses()

        # Figure out object (or model) name.
        queryset = getattr(self.view, 'queryset', None)
        if queryset:
            model = queryset.model
            if hasattr(model._meta, 'verbose_name'):
                object_name = model._meta.verbose_name
            else:
                object_name = model.__name__
        else:
            object_name = 'Object'

        # Add additional response HTTP status codes.
        if self.view.permission_classes:
            if permissions.AllowAny not in self.view.permission_classes:
                ret[status.HTTP_403_FORBIDDEN] = 'Forbidden'
                if self.view.authentication_classes:
                    ret[status.HTTP_401_UNAUTHORIZED] = 'Unauthorized'

        if not is_list_view(self.path, self.method, self.view) and self.method.lower() in ('get', 'put', 'patch'):
            ret[status.HTTP_404_NOT_FOUND] = '{} not found'.format(object_name)

        return ret

    def get_operation_id(self, operation_keys):
        keys = operation_keys[:]

        # Remove the catalog from the operation ID if the operation is not directly about the catalog.
        if len(keys) > 2:
            keys = keys[1:]
        return super().get_operation_id(keys)

    def get_tags(self, operation_keys):
        keys = operation_keys[:]

        # Similar to the operation ID, we want to group by one level deeper than catalog. Otherwise everything will be
        # under the Catalog group.
        if len(keys) > 2:
            keys = keys[1:]
        return super().get_tags(keys)
