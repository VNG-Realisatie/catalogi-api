from django.utils.translation import ugettext_lazy as _

import coreapi
import coreschema
from drf_openapi import codec as openapi_renderers
from drf_openapi.entities import (
    OpenApiSchemaGenerator as _OpenApiSchemaGenerator
)
from rest_framework import exceptions, permissions, renderers, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger import renderers as swagger_renderers


class RedocUIRenderer(swagger_renderers.SwaggerUIRenderer):
    template = 'redoc/index.html'


class OpenApiSchemaGenerator(_OpenApiSchemaGenerator):
    def get_paginator_serializer(self, view, child_serializer_class):
        """
        Overridden to use the `HALPagination` format.
        """
        class HALPaginationSerializer(serializers.Serializer):
            """
            This serializer is not needed for the pagination but for the DRF OpenAPI documentation. It's based on
            `drf_openapi.entities.OpenApiSchemaGenerator.get_paginator_serializer` that defines protected serializer
            classes that do not allow for much customization.
            """
            class LinksSerializer(serializers.Serializer):
                self = serializers.URLField(required=True, help_text=_('URL naar de huidige pagina van de resultaten set.'))
                first = serializers.URLField(required=False, help_text=_('URL naar de eerste pagina van de resultaten set.'))
                prev = serializers.URLField(required=False, help_text=_('URL naar de vorige pagina van de resultaten set.'))
                next = serializers.URLField(required=False, help_text=_('URL naar de volgende pagina van de resultaten set.'))
                last = serializers.URLField(required=False, help_text=_('URL naar de laatste pagina van de resultaten set.'))

            _links = LinksSerializer(required=True, help_text='Meta data over de resultaten set.')
            results = child_serializer_class(many=True)

        return HALPaginationSerializer


class OpenAPISchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = (permissions.AllowAny, )

    renderer_classes = (
        renderers.CoreJSONRenderer,
        openapi_renderers.OpenAPIRenderer,
        # Swagger alternative:
        # swagger_renderers.OpenAPIRenderer,
        RedocUIRenderer,
        # Classic Swagger UI:
        # swagger_renderers.SwaggerUIRenderer,
    )
    url = ''
    title = 'Zaaktypecatalogus API Documentatie'

    def get(self, request, version):
        generator = OpenApiSchemaGenerator(
            version=version,
            url=self.url,
            title=self.title
        )
        # Swagger alternative:
        # from rest_framework.schemas import SchemaGenerator
        # generator = SchemaGenerator()

        schema = generator.get_schema(request=request, public=True)

        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )

        return Response(schema)
