from rest_framework import viewsets

from ...datamodel.models import RolType
from ..serializers import RolTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class RolTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van ROLTYPEn.
    wordt.

    list:
    Een verzameling van ROLTYPEn.
    """
    queryset = RolType.objects.all()
    serializer_class = RolTypeSerializer

    filter_fields = ('roltypeomschrijving', 'is_van')
    ordering_fields = filter_fields
    search_fields = filter_fields
