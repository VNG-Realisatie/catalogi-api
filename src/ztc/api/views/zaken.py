from rest_framework import viewsets

from ...datamodel.models import ZaakObjectType, ZaakType
from ..serializers import ZaakObjectTypeSerializer, ZaakTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import (
    FilterSearchOrderingViewSetMixin, NestedViewSetMixin
)


class ZaakObjectTypeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin,
                            FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De objecttypen van objecten waarop een zaak van het ZAAKTYPE betrekking kan hebben.

    list:
    Een verzameling van ZAAKOBJECTTYPEn.
    """
    queryset = ZaakObjectType.objects.all()
    serializer_class = ZaakObjectTypeSerializer


class ZaakTypeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin,
                      FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Het geheel van karakteristieke eigenschappen van zaken van eenzelfde soort.

    list:
    Een verzameling van ZAAKTYPEn.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer
