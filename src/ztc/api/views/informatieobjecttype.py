from rest_framework import viewsets

from ...datamodel.models import InformatieObjectType
from ..serializers import InformatieObjectTypeSerializer
from ..utils.viewsets import NestedViewSetMixin


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
