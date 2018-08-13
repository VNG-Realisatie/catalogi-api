from rest_framework import viewsets

from ...datamodel.models import RolType
from ..serializers import RolTypeSerializer
from ..utils.viewsets import NestedViewSetMixin


class RolTypeViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Generieke aanduiding van de aard van een ROL die een BETROKKENE kan uitoefenen in ZAAKen van een ZAAKTYPE.

    list:
    Een verzameling van ROLTYPEn.
    """
    queryset = RolType.objects.prefetch_related('mogelijkebetrokkene_set')
    serializer_class = RolTypeSerializer
    pagination_class = None
    lookup_field = 'uuid'
