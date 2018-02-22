from rest_framework import viewsets

from ...datamodel.models import StatusType
from ..serializers import StatusTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import (
    FilterSearchOrderingViewSetMixin, NestedViewSetMixin
)


class StatusTypeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin, FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Generieke aanduiding van de aard van een status.

    list:
    Een verzameling van STATUSTYPEn.
    """
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer
