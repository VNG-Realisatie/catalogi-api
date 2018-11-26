from rest_framework import viewsets
from zds_schema.viewsets import NestedViewSetMixin

from ...datamodel.models import StatusType
from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import StatusTypeSerializer


class StatusTypeViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Generieke aanduiding van de aard van een status.

    list:
    Een verzameling van STATUSTYPEn.
    """
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
