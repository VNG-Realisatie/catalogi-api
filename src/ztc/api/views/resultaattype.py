from rest_framework import viewsets
from vng_api_common.viewsets import NestedViewSetMixin

from ...datamodel.models import ResultaatType
from ..filters import ResultaatTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import ResultaatTypeSerializer


class ResultaatTypeViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Het betreft de indeling of groepering van resultaten van zaken van hetzelfde
    ZAAKTYPE naar hun aard, zoals 'verleend', 'geweigerd', 'verwerkt', etc.

    list:
    Een verzameling van RESULTAATTYPEn.
    """
    queryset = ResultaatType.objects.all()
    serializer_class = ResultaatTypeSerializer
    filter_class = ResultaatTypeFilter
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
