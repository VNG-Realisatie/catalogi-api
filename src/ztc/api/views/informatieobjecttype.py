from rest_framework import viewsets
from vng_api_common.viewsets import NestedViewSetMixin

from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import InformatieObjectTypeSerializer
from ...datamodel.models import InformatieObjectType


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
