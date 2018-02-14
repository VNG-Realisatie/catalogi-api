from rest_framework import viewsets

from ...datamodel.models import StatusType
from ..serializers import StatusTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class StatusTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van STATUSTYPEn.
    wordt.

    list:
    Een verzameling van STATUSTYPEn.
    """
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer

    filter_fields = ('statustype_omschrijving', 'is_van')
    ordering_fields = filter_fields
    search_fields = filter_fields
