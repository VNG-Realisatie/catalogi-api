from rest_framework import viewsets
from zds_schema.viewsets import NestedViewSetMixin

from ...datamodel.models import ZaakObjectType, ZaakType
from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import ZaakObjectTypeSerializer, ZaakTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import FilterSearchOrderingViewSetMixin


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

    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }


class ZaakTypeViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Het geheel van karakteristieke eigenschappen van zaken van eenzelfde soort.

    list:
    Een verzameling van ZAAKTYPEn.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer
    pagination_class = None
    lookup_field = 'uuid'

    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
