from rest_framework import viewsets
from zds_schema.viewsets import NestedViewSetMixin

from ...datamodel.models import InformatieObjectType
from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import InformatieObjectTypeSerializer


class InformatieObjectTypeViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Aanduiding van de aard van INFORMATIEOBJECTTYPEn zoals gehanteerd door de zaakbehandelende organisatie.

    list:
    Een verzameling van INFORMATIEOBJECTTYPEn.
    """
    queryset = InformatieObjectType.objects.all()
    serializer_class = InformatieObjectTypeSerializer
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
