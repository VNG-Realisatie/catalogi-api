from rest_framework import viewsets

from ztc.datamodel.models import Eigenschap

from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import EigenschapSerializer


class EigenschapViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Een relevant inhoudelijk gegeven dat bij ZAAKen van dit ZAAKTYPE geregistreerd moet kunnen worden en geen standaard
    kenmerk is van een zaak.

    list:
    Een verzameling van EIGENSCHAPpen.
    """
    queryset = Eigenschap.objects.all()
    serializer_class = EigenschapSerializer
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
