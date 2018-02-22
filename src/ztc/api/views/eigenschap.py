from rest_framework import viewsets

from ...datamodel.models import Eigenschap
from ..serializers import EigenschapSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import (
    FilterSearchOrderingViewSetMixin, NestedViewSetMixin
)


class EigenschapViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin, FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Een relevant inhoudelijk gegeven dat bij ZAAKen van dit ZAAKTYPE geregistreerd moet kunnen worden en geen standaard
    kenmerk is van een zaak.

    list:
    Een verzameling van EIGENSCHAPpen.
    """
    queryset = Eigenschap.objects.all()
    serializer_class = EigenschapSerializer
