import logging

from django.utils.functional import cached_property, empty

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import (
    CoreAPICompatInspector, FieldInspector, NotHandled, SwaggerAutoSchema
)
from drf_yasg.utils import is_list_view
from drf_yasg.views import get_schema_view
from rest_framework import filters, permissions, serializers, status

from .utils.pagination import HALPaginationInspector

logger = logging.getLogger(__name__)

schema_view = get_schema_view(
    # validators=['flex', 'ssv'],
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


class RelatedFieldDescriptionHelperInspector(FieldInspector):
    """
    This helper adds a description to the n-to serializers. Typically, the (``Nested``)``HyperlinkedRelatedField``
    where ``many=True``, but also the ``ManyToManyField``.

    The description indicates to which resource the URI's point.
    """

    def process_result(self, result, method_name, obj, **kwargs):
        model = self.view.queryset.model

        if isinstance(obj, serializers.ManyRelatedField):
            description = getattr(result, 'description', empty)
            if description is empty:
                field = getattr(model, obj.source)
                if getattr(field, 'reverse', True):
                    related_model_name = field.rel.related_model.__name__.upper()
                else:
                    related_model_name = field.rel.model.__name__.upper()
                result.description = 'Zero or more URI\'s to a {}'.format(related_model_name)
        elif isinstance(obj, serializers.RelatedField):
            description = getattr(result, 'description', empty)
            if description is empty:
                if obj.source != '*':
                    source_model = getattr(model, obj.source)
                    if hasattr(source_model, 'rel'):
                        related_model = source_model.rel.related_model
                    else:
                        related_model = source_model.field.related_model
                    related_model_name = related_model.__name__.upper()
                    result.description = 'URI to a {}'.format(related_model_name)
        return super().process_result(result, method_name, obj, **kwargs)


class AutoSchema(SwaggerAutoSchema):
    field_inspectors = [
        RelatedFieldDescriptionHelperInspector,
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS
    filter_inspectors = [
        DjangoFilterDescriptionInspector,
        SearchDescriptionInspector,
        OrderingDescriptionInspector,
    ] + swagger_settings.DEFAULT_FILTER_INSPECTORS
    paginator_inspectors = [
        HALPaginationInspector
    ] + swagger_settings.DEFAULT_PAGINATOR_INSPECTORS

    @cached_property
    def model(self):
        if hasattr(self.view, 'queryset'):
            return self.view.queryset.model

        return None

    def get_default_responses(self):
        """Get the default responses determined for this view from the request serializer and request method.

        :type: dict[str, openapi.Schema]
        """
        ret = super().get_default_responses()

        # Figure out object (or model) name.
        if self.model:
            if hasattr(self.model._meta, 'verbose_name'):
                object_name = self.model._meta.verbose_name
            else:
                object_name = self.model.__name__
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
        """
        Simply return the model name as lowercase string, postfixed with the operation name.
        """
        model_name = self.model.__name__.lower()
        return '_'.join([model_name, operation_keys[-1]])

    def get_tags(self, operation_keys):
        keys = operation_keys[:]

        # Similar to the operation ID, we want to group by one level deeper than catalog. Otherwise everything will be
        # under the Catalog group.
        if len(keys) > 2:
            keys = keys[1:]
        return super().get_tags(keys)

    def get_description(self):
        description = self.overrides.get('operation_description', None)
        if description is None:
            model_name = self.model.__name__.upper()
            description = '**Objecttype {}**\n\n{}'.format(
                model_name,
                self._sch.get_description(self.path, self.method),
            )
        return description
