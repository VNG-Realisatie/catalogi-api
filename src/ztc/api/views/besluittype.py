from rest_framework import mixins, viewsets

from ...datamodel.models import BesluitType
from ..filters import BesluitTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import BesluitTypeSerializer
from .mixins import DraftMixin


class BesluitTypeViewSet(DraftMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.ReadOnlyModelViewSet):
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
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
        'publish': SCOPE_ZAAKTYPES_WRITE,
    }
