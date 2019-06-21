from rest_framework import mixins, viewsets

from ...datamodel.models import StatusType
from ..filters import StatusTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import StatusTypeSerializer
from .mixins import ZaakTypeDraftDestroyMixin


class StatusTypeViewSet(ZaakTypeDraftDestroyMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.ReadOnlyModelViewSet):
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
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }
