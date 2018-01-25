from rest_framework import viewsets

from ...datamodel.models import Catalogus
from ..utils.rest_flex_fields import FlexFieldsMixin
from .serializers import CatalogusSerializer


class CatalogusViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKTYPEn - incl. daarvoor relevante objecttypen - voor een Domein die als één geheel beheerd
    wordt.

    list:
    Een verzameling van CATALOGUSsen.
    """
    # This makes the URLs consistent with `NestedSimpleRouter`, which uses `<prefix>_id` instead of `<prefix>_pk`.
    # lookup_url_kwarg = 'id'

    queryset = Catalogus.objects.all()
    serializer_class = CatalogusSerializer

    # Typically, the filter-, ordering- and search fields, should be the same as used in the admin.
    filter_fields = ('domein', 'rsin', )
    ordering_fields = filter_fields

    search_fields = filter_fields + ('contactpersoon_beheer_naam', )
