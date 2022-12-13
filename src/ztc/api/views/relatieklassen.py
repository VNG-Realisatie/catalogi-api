from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import InformatieObjectType, ZaakInformatieobjectType, ZaakType
from ..filters import ZaakInformatieobjectTypeFilter
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import ZaakTypeInformatieObjectTypeSerializer
from ..utils.viewsets import build_absolute_url, is_url
from .mixins import ConceptFilterMixin, ForcedCreateUpdateMixin


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary=_("Alle ZAAKTYPE-INFORMATIEOBJECTTYPE relaties opvragen."),
        description=_("Deze lijst kan gefilterd wordt met query-string parameters."),
    ),
    retrieve=extend_schema(
        summary=_("Een specifieke ZAAKTYPE-INFORMATIEOBJECTTYPE relatie opvragen."),
        description=_("Een specifieke ZAAKTYPE-INFORMATIEOBJECTTYPE relatie opvragen."),
    ),
    create=extend_schema(
        summary=_("Maak een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie aan."),
        description=_(
            "Maak een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie aan. Dit kan alleen als het"
            " bijbehorende ZAAKTYPE een concept betreft. Er wordt gevalideerd op:\n"
            "- `zaaktype` en `informatieobjecttype` behoren tot dezelfde `catalogus`"
        ),
    ),
    update=extend_schema(
        summary=_("Werk een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie in zijn geheel bij."),
        description=_(
            "Werk een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie in zijn geheel bij. "
            "Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft. "
            "Er wordt gevalideerd op:\n"
            " - `zaaktype` en `informatieobjecttype` behoren tot dezelfde `catalogus`"
        ),
    ),
    partial_update=extend_schema(
        summary=_("Werk een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie deels bij."),
        description=_(
            "Werk een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie deels bij. "
            "Dit kan alleen  als het bijbehorende ZAAKTYPE een concept betreft.  "
            "Er wordt gevalideerd op:\n"
            "  - `zaaktype` en `informatieobjecttype` behoren tot dezelfde `catalogus`"
        ),
    ),
    destroy=extend_schema(
        summary=_("Verwijder een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie."),
        description=_(
            "Verwijder een ZAAKTYPE-INFORMATIEOBJECTTYPE relatie. "
            "Dit kan alleen als  het bijbehorende ZAAKTYPE een concept betreft."
            " Er wordt gevalideerd op:\n"
            "  - `zaaktype` of `informatieobjecttype` is nog niet gepubliceerd"
        ),
    ),
)
class ZaakTypeInformatieObjectTypeViewSet(
    CheckQueryParamsMixin,
    ConceptFilterMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    global_description = (
        "Opvragen en bewerken van ZAAKTYPE-INFORMATIEOBJECTTYPE relaties. Geeft aan welke "
        "INFORMATIEOBJECTTYPEn binnen een ZAAKTYPE mogelijk zijn en hoe de richting is."
    )

    queryset = ZaakInformatieobjectType.objects.all().order_by("-pk")
    serializer_class = ZaakTypeInformatieObjectTypeSerializer
    filterset_class = ZaakInformatieobjectTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
    }

    def get_concept(self, instance):
        ziot = self.get_object()
        zaaktype = getattr(instance, "zaaktype", None) or ziot.zaaktype
        informatieobjecttype = (
            getattr(instance, "informatieobjecttype", None) or ziot.informatieobjecttype
        )
        return zaaktype.concept or informatieobjecttype.concept

    def get_concept_filter(self):
        return ~(Q(zaaktype__concept=True) | Q(informatieobjecttype__concept=True))

    def perform_destroy(self, instance):
        forced_delete = self.request.jwt_auth.has_auth(
            scopes=SCOPE_CATALOGI_FORCED_DELETE
        )

        if not forced_delete:
            if not self.get_concept(instance):
                msg = _("Objects related to non-concept objects can't be destroyed")
                raise ValidationError(
                    {"nonFieldErrors": msg}, code="non-concept-relation"
                )

        super().perform_destroy(instance)

    def create(self, request, *args, **kwargs):
        request = self.zaaktype_informatieobjecttype_to_url(request)
        return super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request = self.zaaktype_informatieobjecttype_to_url(request)
        return super(viewsets.ModelViewSet, self).update(request, *args, **kwargs)

    # def zaaktype_informatieobjecttype_to_url(self, request):
    #     """
    #     The arrays of 'zaaktype_identificaties' and 'informatieobjecttype_omschrijving' are transformed to an array of urls, which are required for the
    #     m2m relationship. The corresponding urls are based on their most recent 'geldigheid' date, denoted by 'datum_einde_geldigheid=None'.
    #     """
    #     # todo discuss proper way to filter this.
    #
    #     urls = {"zaaktype": "", "informatieobjecttype": ""}
    #     if identificatie := request.data.get("zaaktype", []):
    #         zaak = ZaakType.objects.filter(
    #             identificatie=identificatie, datum_einde_geldigheid=None, concept=False
    #         )
    #         if not zaak:
    #             zaak = ZaakType.objects.filter(
    #                 identificatie=identificatie,
    #                 datum_einde_geldigheid=None,
    #                 concept=True,
    #             )
    #
    #         urls[
    #             "zaaktype"
    #         ] = f"{build_absolute_url(self.action, request)}/zaaktypen/{str(zaak[0].uuid)}"
    #         request.data["zaaktype"] = urls["zaaktype"]
    #
    #     if omschrijving := request.data.get("informatieobjecttype", []):
    #         informatieobjecttype = InformatieObjectType.objects.filter(
    #             omschrijving=omschrijving, datum_einde_geldigheid=None, concept=False
    #         )
    #         if not informatieobjecttype:
    #             informatieobjecttype = InformatieObjectType.objects.filter(
    #                 omschrijving=omschrijving, datum_einde_geldigheid=None, concept=True
    #             )
    #
    #         urls[
    #             "informatieobjecttype"
    #         ] = f"{build_absolute_url(self.action, request)}/informatieobjecttypen/{str(informatieobjecttype[0].uuid)}"
    #
    #         request.data["informatieobjecttype"] = urls["informatieobjecttype"]
    #
    #     return request
