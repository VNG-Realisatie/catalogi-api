from rest_framework import mixins, viewsets

from ...datamodel.models import ResultaatType
from ..filters import ResultaatTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import ResultaatTypeSerializer
from .mixins import ZaakTypeDraftDestroyMixin


class ResultaatTypeViewSet(ZaakTypeDraftDestroyMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.ReadOnlyModelViewSet):
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
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }
