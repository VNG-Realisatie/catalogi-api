from rest_framework import viewsets

from ...datamodel.models import ZaakTypenRelatie
from ..serializers import ZaakTypenRelatieSerializer
from ..utils.rest_flex_fields import FlexFieldsMixin


class ZaakTypenRelatieViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ZaakTypenRelatie.objects.all()
    serializer_class = ZaakTypenRelatieSerializer

    filter_fields = ('zaaktype_van', 'zaaktype_naar')
    ordering_fields = filter_fields
    search_fields = filter_fields
