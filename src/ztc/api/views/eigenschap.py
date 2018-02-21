from rest_framework import viewsets

from ...datamodel.models import Eigenschap
from ..serializers import EigenschapSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class EigenschapViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Een relevant inhoudelijk gegeven dat bij ZAAKen van dit ZAAKTYPE geregistreerd moet kunnen worden en geen standaard
    kenmerk is van een zaak.

    list:
    Een verzameling van EIGENSCHAPpen.
    """
    queryset = Eigenschap.objects.all()
    serializer_class = EigenschapSerializer

    filter_fields = ('eigenschapnaam', 'is_van')
    ordering_fields = filter_fields
    search_fields = filter_fields
