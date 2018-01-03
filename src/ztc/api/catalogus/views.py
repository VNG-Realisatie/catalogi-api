from rest_framework import viewsets
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

from .serializers import CatalogusSerializer
from ...datamodel.models import Catalogus


class CatalogusViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Catalogus.objects.all()
    serializer_class = CatalogusSerializer
