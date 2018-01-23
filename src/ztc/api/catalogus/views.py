import coreapi
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import viewsets
from rest_framework.schemas import AutoSchema

from ...datamodel.models import Catalogus
from .serializers import CatalogusSerializer


class CatalogusViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKTYPEn - incl. daarvoor relevante objecttypen - voor een Domein die als één geheel beheerd
    wordt.

    list:
    Een verzameling van CATALOGUSsen.
    """
    queryset = Catalogus.objects.all()
    # TODO: This serializer is slightly odd, since its not versioned.
    serializer_class = CatalogusSerializer
    filter_fields = ('domein', 'rsin', )
    ordering_fields = filter_fields
    search_fields = filter_fields + ('contactpersoon_beheer_naam', )

    #
    # # NOTE: This decorator is needed to work with DRF OpenAPI schema's.
    # @view_config(request_serializer=CatalogusSerializer, response_serializer=CatalogusSerializer)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # NOTE: This does not work with DRF OpenAPI schema's.
    # TODO: Move to generic view section.
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('expand', description='Which field(s) to expand. Multiple fields can be separated with a comma.'),
            coreapi.Field('fields', description='Which field(s) to show. Multiple fields can be separated with a comma.'),
        ]
    )


# TODO:
# https://github.com/seebass/drf-hal-json
# http://jpadilla.github.io/django-rest-framework-xml/
