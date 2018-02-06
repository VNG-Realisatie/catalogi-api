from rest_framework import viewsets

from ...datamodel.models import ZaakType
from ..serializers import ZaakTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class ZaakTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ZAAKTYPEs.
    wordt.

    list:
    Een verzameling van ZAAKTYPEs.
    """
    queryset = ZaakType.objects.all()
    serializer_class = ZaakTypeSerializer

    filter_fields = ('maakt_deel_uit_van',)
    ordering_fields = filter_fields
    search_fields = filter_fields
