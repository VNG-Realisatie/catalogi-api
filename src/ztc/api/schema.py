from drf_openapi import codec as openapi_renderers
from drf_openapi.entities import OpenApiSchemaGenerator
from rest_framework import exceptions, permissions, renderers
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers as swagger_renderers


class RedocUIRenderer(swagger_renderers.SwaggerUIRenderer):
    template = 'redoc/index.html'


class OpenAPISchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = (permissions.AllowAny, )

    renderer_classes = (
        renderers.CoreJSONRenderer,
        openapi_renderers.OpenAPIRenderer,
        RedocUIRenderer,
    )
    url = ''
    title = 'Zaaktypecatalogus API Documentation'

    def get(self, request, version):
        generator = OpenApiSchemaGenerator(
            version=version,
            url=self.url,
            title=self.title
        )
        schema = generator.get_schema(request=request, public=True)

        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )

        return Response(schema)


class SwaggerSchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True

    permission_classes = (permissions.AllowAny, )
    renderer_classes = (
        renderers.CoreJSONRenderer,
        swagger_renderers.OpenAPIRenderer,
        # swagger_renderers.SwaggerUIRenderer,
        RedocUIRenderer
    )

    def get(self, request, *args, **kwargs):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request, public=True)

        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )

        return Response(schema)
