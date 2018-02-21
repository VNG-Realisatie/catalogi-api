from rest_framework import viewsets

from ...datamodel.models import ZaakObjectType, ZaakType
from ..serializers import ZaakObjectTypeSerializer, ZaakTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class ZaakObjectTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De objecttypen van objecten waarop een zaak van het ZAAKTYPE betrekking kan hebben.

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
    Het geheel van karakteristieke eigenschappen van zaken van eenzelfde soort.

    list:
    Een verzameling van ZAAKTYPEn.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer

    filter_fields = ('maakt_deel_uit_van',)
    ordering_fields = filter_fields
    search_fields = filter_fields
