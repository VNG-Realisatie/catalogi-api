from rest_framework import viewsets

from .serializers import BesluitTypeSerializer
from ...datamodel.models import BesluitType


class BesluitTypeViewSet(viewsets.ModelViewSet):
    queryset = BesluitType.objects.all()
    serializer_class = BesluitTypeSerializer
