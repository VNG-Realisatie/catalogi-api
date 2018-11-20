from rest_framework import viewsets

from ztc.datamodel.models import Catalogus

from ..scopes import SCOPE_ZAAKTYPES_READ
from ..serializers import CatalogusSerializer


class CatalogusViewSet(viewsets.ReadOnlyModelViewSet):
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
    }
