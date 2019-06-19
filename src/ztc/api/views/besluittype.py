from rest_framework import viewsets

from ...datamodel.models import BesluitType
from ..filters import BesluitTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import BesluitTypeSerializer


class BesluitTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Generieke aanduiding van de aard van een besluit.

    list:
    Alle BESLUITTYPEn van de besluiten die het resultaat kunnen zijn van het
    zaakgericht werken van de behandelende organisatie(s).
    """
    queryset = BesluitType.objects.all()
    serializer_class = BesluitTypeSerializer
    filterset_class = BesluitTypeFilter
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
