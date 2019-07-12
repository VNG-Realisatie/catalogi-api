from django.utils.translation import ugettext_lazy as _

from rest_framework import mixins, viewsets
from rest_framework.exceptions import PermissionDenied

from ...datamodel.models import (
    ZaakInformatieobjectType
)
from ..filters import ZaakInformatieobjectTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import (
    ZaakTypeInformatieObjectTypeSerializer
)
from .mixins import ConceptDestroyMixin, ConceptFilterMixin


class ZaakTypeInformatieObjectTypeViewSet(ConceptFilterMixin,
                                          ConceptDestroyMixin,
                                          mixins.CreateModelMixin,
                                          mixins.DestroyModelMixin,
                                          viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Relatie met informatieobjecttype dat relevant is voor zaaktype.

    list:
    Een verzameling van ZAAKINFORMATIEOBJECTTYPEn.

    Filteren van de gegevens kan middels de querystringparameters:
    - zaaktype: URL van het zaaktype
    - informatie_object_type: URL van het zaaktype
    - richting: waarde van de richting (string)

    Meerdere querystring-parameters tegelijk worden als een AND beschouwd.
    """
    queryset = ZaakInformatieobjectType.objects.all().order_by('-pk')
    serializer_class = ZaakTypeInformatieObjectTypeSerializer
    filterset_class = ZaakInformatieobjectTypeFilter
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }

    def get_concept(self, instance):
        return instance.zaaktype.concept and instance.informatie_object_type.concept

    def perform_create(self, serializer):
        zaaktype = serializer.validated_data['zaaktype']
        informatie_object_type = serializer.validated_data['informatie_object_type']

        if not(zaaktype.concept and informatie_object_type.concept):
            msg = _("Creating relations between non-concept objects is forbidden")
            raise PermissionDenied(detail=msg)
        super().perform_create(serializer)

    def get_concept_filter(self):
        return {'zaaktype__concept': False, 'informatie_object_type__concept': False}


# class ZaakInformatieobjectTypeArchiefregimeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin,
#                                                    FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
#     """
#     retrieve:
#     Afwijkende archiveringskenmerken van informatieobjecten van een INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op
#     grond van resultaten van een RESULTAATTYPE bij dat ZAAKTYPE.
#
#     list:
#     Een verzameling van ZAAKINFORMATIEOBJECTTYPEARCHIEFREGIMEs.
#     """
#     queryset = ZaakInformatieobjectTypeArchiefregime.objects.all()
#     serializer_class = ZaakInformatieobjectTypeArchiefregimeSerializer
#     required_scopes = {
#         'list': SCOPE_ZAAKTYPES_READ,
#         'retrieve': SCOPE_ZAAKTYPES_READ,
#     }
