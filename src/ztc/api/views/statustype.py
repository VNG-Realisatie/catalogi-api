from rest_framework import viewsets

from ...datamodel.models import StatusType
from ..serializers import StatusTypeSerializer
from ..utils.viewsets import NestedViewSetMixin


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
