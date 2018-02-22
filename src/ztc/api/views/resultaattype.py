from rest_framework import viewsets

from ...datamodel.models import ResultaatType
from ..serializers import ResultaatTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import (
    FilterSearchOrderingViewSetMixin, NestedViewSetMixin
)


class ResultaatTypeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin, FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Het betreft de indeling of groepering van resultaten van zaken van hetzelfde ZAAKTYPE naar hun aard, zoals
    'verleend', 'geweigerd', 'verwerkt', etc.

    list:
    Een verzameling van RESULTAATTYPEn.
    """
    queryset = ResultaatType.objects.all()
    serializer_class = ResultaatTypeSerializer
