from rest_framework import viewsets

from ...datamodel.models import ZaakInformatieobjectType, ZaakTypenRelatie
from ..serializers import (
    InformatieObjectTypeZaakTypeSerializer,
    ZaakTypeInformatieObjectTypeSerializer, ZaakTypenRelatieSerializer
)
from ..utils.rest_flex_fields import FlexFieldsMixin


class ZaakTypenRelatieViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ZaakTypenRelatie.objects.all()
    serializer_class = ZaakTypenRelatieSerializer

    filter_fields = ('zaaktype_van', 'zaaktype_naar')
    ordering_fields = filter_fields
    search_fields = filter_fields


class ZaakTypeInformatieObjectTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ZaakInformatieobjectType.objects.all()
    serializer_class = ZaakTypeInformatieObjectTypeSerializer

    filter_fields = ('zaaktype', 'informatie_object_type')
    ordering_fields = filter_fields
    search_fields = filter_fields


class InformatieObjectTypeZaakTypeSerializerViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ZaakInformatieobjectType.objects.all()
    serializer_class = InformatieObjectTypeZaakTypeSerializer

    filter_fields = ('zaaktype', 'informatie_object_type')
    ordering_fields = filter_fields
    search_fields = filter_fields
