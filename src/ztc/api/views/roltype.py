from rest_framework import viewsets, mixins
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import RolType
from ..filters import RolTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import RolTypeSerializer
from .mixins import ZaakTypeDraftDestroyMixin


class RolTypeViewSet(CheckQueryParamsMixin,
                     ZaakTypeDraftDestroyMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Generieke aanduiding van de aard van een ROL die een BETROKKENE kan uitoefenen in ZAAKen van een ZAAKTYPE.

    list:
    Een verzameling van ROLTYPEn.
    """
    queryset = RolType.objects.prefetch_related('mogelijkebetrokkene_set')
    serializer_class = RolTypeSerializer
    filterset_class = RolTypeFilter
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }
