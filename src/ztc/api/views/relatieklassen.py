from django.utils.translation import ugettext_lazy as _

from rest_framework import mixins, viewsets
from rest_framework.exceptions import PermissionDenied
from vng_api_common.viewsets import NestedViewSetMixin

from ...datamodel.models import (
    ZaakInformatieobjectType, ZaakInformatieobjectTypeArchiefregime
)
from ..filters import ZaakInformatieobjectTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import (
    ZaakInformatieobjectTypeArchiefregimeSerializer,
    ZaakTypeInformatieObjectTypeSerializer
)
from ..utils.rest_flex_fields import FlexFieldsMixin
from ..utils.viewsets import FilterSearchOrderingViewSetMixin
from .mixins import DraftDestroyMixin


class ZaakTypeInformatieObjectTypeViewSet(DraftDestroyMixin,
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
    queryset = ZaakInformatieobjectType.objects.all()
    serializer_class = ZaakTypeInformatieObjectTypeSerializer
    filterset_class = ZaakInformatieobjectTypeFilter
    lookup_field = 'uuid'
    pagination_class = None
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }

    def get_draft(self, instance):
        return instance.zaaktype.draft and instance.informatie_object_type.draft

    def perform_create(self, serializer):
        zaaktype = serializer.validated_data['zaaktype']
        informatie_object_type = serializer.validated_data['informatie_object_type']

        if not(zaaktype.draft and informatie_object_type.draft):
            msg = _("Creating relations between non-draft objects is forbidden")
            raise PermissionDenied(detail=msg)
        super().perform_create(serializer)


class ZaakInformatieobjectTypeArchiefregimeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin,
                                                   FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Afwijkende archiveringskenmerken van informatieobjecten van een INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op
    grond van resultaten van een RESULTAATTYPE bij dat ZAAKTYPE.

    list:
    Een verzameling van ZAAKINFORMATIEOBJECTTYPEARCHIEFREGIMEs.
    """
    queryset = ZaakInformatieobjectTypeArchiefregime.objects.all()
    serializer_class = ZaakInformatieobjectTypeArchiefregimeSerializer
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
    }
