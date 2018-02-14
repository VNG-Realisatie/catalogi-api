from rest_framework import viewsets

from ...datamodel.models import ResultaatType
from ..serializers import ResultaatTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class ResultaatTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    De verzameling van RESULTAATTYPEn.
    wordt.

    list:
    Een verzameling van RESULTAATTYPEn.
    """
    queryset = ResultaatType.objects.all()
    serializer_class = ResultaatTypeSerializer

    filter_fields = ('resultaattypeomschrijving', 'selectielijstklasse')
    ordering_fields = filter_fields
    search_fields = filter_fields
