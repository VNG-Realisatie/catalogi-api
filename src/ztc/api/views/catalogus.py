from rest_framework import viewsets

from ...datamodel.models import Catalogus
from ..serializers import CatalogusSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import (
    FilterSearchOrderingViewSetMixin, NestedViewSetMixin
)


class CatalogusViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin, FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
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
