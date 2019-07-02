from rest_framework import mixins, viewsets

from ...datamodel.models import InformatieObjectType
from ..filters import InformatieObjectTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import InformatieObjectTypeSerializer
from .mixins import ConceptMixin


class InformatieObjectTypeViewSet(ConceptMixin,
                                  mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Aanduiding van de aard van INFORMATIEOBJECTTYPEn zoals gehanteerd door de zaakbehandelende organisatie.

    list:
    Een verzameling van INFORMATIEOBJECTTYPEn.
    """
    queryset = InformatieObjectType.objects.all()
    serializer_class = InformatieObjectTypeSerializer
    filterset_class = InformatieObjectTypeFilter
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
        'publish': SCOPE_ZAAKTYPES_WRITE,
    }
