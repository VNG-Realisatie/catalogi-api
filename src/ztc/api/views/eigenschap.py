from rest_framework import mixins, viewsets

from ztc.datamodel.models import Eigenschap

from ..filters import EigenschapFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import EigenschapSerializer
from .mixins import ZaakTypeDraftDestroyMixin


class EigenschapViewSet(ZaakTypeDraftDestroyMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Een relevant inhoudelijk gegeven dat bij ZAAKen van dit ZAAKTYPE geregistreerd moet kunnen worden en geen standaard
    kenmerk is van een zaak.

    list:
    Een verzameling van EIGENSCHAPpen.
    """
    queryset = Eigenschap.objects.all()
    serializer_class = EigenschapSerializer
    filterset_class = EigenschapFilter
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }
