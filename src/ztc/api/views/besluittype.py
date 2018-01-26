from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import viewsets

from ...datamodel.models import BesluitType
from ..serializers import BesluitTypeSerializer


class BesluitTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = BesluitType.objects.all()
    serializer_class = BesluitTypeSerializer
