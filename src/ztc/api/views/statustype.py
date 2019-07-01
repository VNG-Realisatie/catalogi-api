from rest_framework import viewsets

from ...datamodel.models import StatusType
from ..filters import StatusTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import StatusTypeSerializer


class StatusTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Generieke aanduiding van de aard van een status.

    list:
    Een verzameling van STATUSTYPEn.
    """
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer
    filterset_class = StatusTypeFilter
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
