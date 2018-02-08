from rest_framework import viewsets

from ...datamodel.models import ZaakType, ZaakObjectType
from ..serializers import ZaakTypeSerializer, ZaakObjectTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class ZaakObjectTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKOBJECTTYPEn.
    wordt.

    list:
    Een verzameling van ZAAKOBJECTTYPEn.
    """
    queryset = ZaakObjectType.objects.all()
    serializer_class = ZaakObjectTypeSerializer

    filter_fields = ('is_relevant_voor',)
    ordering_fields = filter_fields
    search_fields = filter_fields


class ZaakTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKTYPEs.
    wordt.

    list:
    Een verzameling van ZAAKTYPEs.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer

    filter_fields = ('maakt_deel_uit_van',)
    ordering_fields = filter_fields
    search_fields = filter_fields
