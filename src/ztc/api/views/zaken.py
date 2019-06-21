from rest_framework import viewsets, mixins
from vng_api_common.viewsets import NestedViewSetMixin

from ...datamodel.models import ZaakObjectType, ZaakType
from ..filters import ZaakTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import ZaakObjectTypeSerializer, ZaakTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import FilterSearchOrderingViewSetMixin
from .mixins import DraftMixin


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


class ZaakTypeViewSet(DraftMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Het geheel van karakteristieke eigenschappen van zaken van eenzelfde soort.

    list:
    Een verzameling van ZAAKTYPEn.
    """
    queryset = ZaakType.objects.prefetch_related(
        'statustypen',
        'zaaktypenrelaties',
        'heeft_relevant_informatieobjecttype',
        'statustypen',
        'resultaattypen',
        'eigenschap_set',
        'roltype_set',
        'besluittype_set',
    )
    serializer_class = ZaakTypeSerializer
    pagination_class = None
    lookup_field = 'uuid'
    filterset_class = ZaakTypeFilter
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
        'publish': SCOPE_ZAAKTYPES_WRITE,

    }
