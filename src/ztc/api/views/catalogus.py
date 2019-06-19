from rest_framework import viewsets, mixins

from ztc.datamodel.models import Catalogus

from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import CatalogusSerializer


class CatalogusViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKTYPEn - incl. daarvoor relevante objecttypen - voor een Domein die als één geheel beheerd
    wordt.

    list:
    Een verzameling van CATALOGUSsen.
    """
    queryset = Catalogus.objects.all()
    serializer_class = CatalogusSerializer
    pagination_class = None
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }
