from rest_framework import viewsets

from ...datamodel.models import (
    ZaakInformatieobjectType, ZaakInformatieobjectTypeArchiefregime,
    ZaakTypenRelatie
)
from ..serializers import (
    ZaakInformatieobjectTypeArchiefregimeSerializer,
    ZaakTypeInformatieObjectTypeSerializer, ZaakTypenRelatieSerializer
)
from ..utils.rest_flex_fields import FlexFieldsMixin


class ZaakTypenRelatieViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Relatie met zaaktype dat gerelateerd is aan het zaaktype.

    list:
    Een verzameling van ZAAKTYPENRELATIEs.
    """
    queryset = ZaakTypenRelatie.objects.all()
    serializer_class = ZaakTypenRelatieSerializer

    filter_fields = ('zaaktype_van', 'zaaktype_naar')
    ordering_fields = filter_fields
    search_fields = filter_fields


class ZaakTypeInformatieObjectTypeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Relatie met informatieobjecttype dat relevant is voor zaaktype.

    list:
    Een verzameling van ZAAKINFORMATIEOBJECTTYPEn.
    """
    queryset = ZaakInformatieobjectType.objects.all()
    serializer_class = ZaakTypeInformatieObjectTypeSerializer

    filter_fields = ('zaaktype', 'informatie_object_type')
    ordering_fields = filter_fields
    search_fields = filter_fields


class ZaakInformatieobjectTypeArchiefregimeViewSet(FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Afwijkende archiveringskenmerken van informatieobjecten van een INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op
    grond van resultaten van een RESULTAATTYPE bij dat ZAAKTYPE.

    list:
    Een verzameling van ZAAKINFORMATIEOBJECTTYPEARCHIEFREGIMEs.
    """
    queryset = ZaakInformatieobjectTypeArchiefregime.objects.all()
    serializer_class = ZaakInformatieobjectTypeArchiefregimeSerializer

    filter_fields = ('zaak_informatieobject_type', 'resultaattype')
    ordering_fields = filter_fields
    search_fields = filter_fields
