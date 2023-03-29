from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings
from vng_api_common.caching import conditional_retrieve
from vng_api_common.schema import COMMON_ERRORS
from vng_api_common.serializers import FoutSerializer, ValidatieFoutSerializer
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import ZaakType
from ..filters import ZaakTypeFilter
from ..kanalen import KANAAL_ZAAKTYPEN
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import (
    ZaakTypeCreateSerializer,
    ZaakTypeSerializer,
    ZaakTypeUpdateSerializer,
)
from ..utils.viewsets import extract_relevant_m2m, m2m_array_of_str_to_url
from .mixins import ConceptMixin, ForcedCreateUpdateMixin, M2MConceptDestroyMixin


@extend_schema_view(
    list=extend_schema(
        summary=_("Alle ZAAKTYPEn opvragen."),
        description=_("Deze lijst kan gefilterd wordt met query-string parameters."),
    ),
    retrieve=extend_schema(
        summary=_("Een specifieke ZAAKTYPE opvragen."),
        description=_("Een specifieke ZAAKTYPE opvragen."),
    ),
    create=extend_schema(
        summary=_("Maak een ZAAKTYPE aan."),
        description=_(
            "Er wordt gevalideerd op:\n"
            "- geldigheid `catalogus` URL, dit moet een catalogus binnen dezelfde API zijn\n"
            " - Uniciteit `catalogus` en `omschrijving`. Dezelfde omeschrijving mag enkel"
            "  opnieuw gebruikt worden als het zaaktype een andere geldigheidsperiode"
            "  kent dan bestaande zaaktypen.\n"
            " - `deelzaaktypen` moeten tot dezelfde catalogus behoren als het ZAAKTYPE."
        ),
    ),
    update=extend_schema(
        summary=_("Werk een ZAAKTYPE in zijn geheel bij."),
        description=_(
            "Werk een ZAAKTYPE in zijn geheel bij. Dit kan alleen als het een concept betreft."
            " Er wordt gevalideerd op:\n"
            "  - `deelzaaktypen` moeten tot dezelfde catalogus behoren als het ZAAKTYPE."
        ),
    ),
    partial_update=extend_schema(
        summary=_("Werk een ZAAKTYPE deels bij."),
        description=_(
            "Werk een ZAAKTYPE deels bij. Dit kan alleen als het een concept betreft."
            " Er wordt gevalideerd op:\n"
            " - `deelzaaktypen` moeten tot dezelfde catalogus behoren als het ZAAKTYPE."
        ),
    ),
    destroy=extend_schema(
        summary=_("Verwijder een ZAAKTYPE."),
        description=_(
            "Verwijder een ZAAKTYPE. Dit kan alleen als het een concept betreft."
        ),
    ),
    publish=extend_schema(
        summary=_("Publiceer het concept ZAAKTYPE."),
        description=_(
            "Publiceren van het zaaktype zorgt ervoor dat dit in een Zaken API kan gebruikt"
            "worden. Na het publiceren van een zaaktype zijn geen inhoudelijke wijzigingen"
            "meer mogelijk - ook niet de statustypen, eigenschappen... etc. Indien er na het"
            "publiceren nog wat gewijzigd moet worden, dan moet je een nieuwe versie"
            "aanmaken."
        ),
    ),
)
@conditional_retrieve()
class ZaakTypeViewSet(
    CheckQueryParamsMixin,
    ConceptMixin,
    M2MConceptDestroyMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    global_description = (
        "Opvragen en bewerken van ZAAKTYPEn nodig voor ZAKEN in de Zaken API."
        "Een ZAAKTYPE beschrijft het geheel van karakteristieke "
        "eigenschappen van zaken van eenzelfde soort."
    )

    queryset = ZaakType.objects.prefetch_related(
        "statustypen",
        "zaaktypenrelaties",
        "informatieobjecttypen",
        "statustypen",
        "resultaattypen",
        "eigenschap_set",
        "roltype_set",
        "besluittypen",
        "objecttypen",
    ).order_by("-pk")
    serializer_class = ZaakTypeSerializer
    lookup_field = "uuid"
    filterset_class = ZaakTypeFilter
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
        "publish": SCOPE_CATALOGI_WRITE,
    }
    concept_related_fields = ["besluittypen", "informatieobjecttypen"]
    notifications_kanaal = KANAAL_ZAAKTYPEN
    relation_fields = ["zaaktypenrelaties"]

    @action(detail=True, methods=["post"])
    @extend_schema(
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: ValidatieFoutSerializer,
            status.HTTP_404_NOT_FOUND: FoutSerializer,
            **{exc.status_code: FoutSerializer for exc in COMMON_ERRORS},
        },
    )
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()
        # check related objects
        if (
            instance.besluittypen.filter(concept=True).exists()
            or instance.informatieobjecttypen.filter(concept=True).exists()
            or instance.deelzaaktypen.filter(concept=True).exists()
        ):
            msg = _("All related resources should be published")
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: msg}, code="concept-relation"
            )

        instance.concept = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    @extend_schema(
        request=ZaakTypeCreateSerializer,
        responses={201: ZaakTypeSerializer},
    )
    def create(self, request, *args, **kwargs):
        request = m2m_array_of_str_to_url(
            request,
            ["besluittypen", "deelzaaktypen", "gerelateerde_zaaktypen"],
            self.action,
        )
        return super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """automatically create new zaaktype relations when creating a new version of a zaaktype"""
        serializer.save()
        if not serializer.data.get("gerelateerde_zaaktypen", []):
            for zaaktype in ZaakType.objects.all():
                for relatie in zaaktype.zaaktypenrelaties.all():
                    uuid = relatie.gerelateerd_zaaktype.split("/")[-1]
                    model = get_object_or_404(ZaakType, uuid=uuid)
                    if model.identificatie == serializer.data.get("identificatie", None):
                        relatie.id = None
                        uuid = serializer.data.get("url", None).split("/")[-1]
                        relatie.gerelateerd_zaaktype = relatie.gerelateerd_zaaktype.rsplit('/', 1)[0] + "/" + str(uuid)
                        relatie.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = extract_relevant_m2m(
            self.get_serializer(instance),
            [
                "besluittypen",
                "informatieobjecttypen",
                "deelzaaktypen",
                "gerelateerde_zaaktypen",
            ],
            self.action,
        )
        return Response(serializer.data)

    @extend_schema(
        request=ZaakTypeUpdateSerializer,
        responses={200: ZaakTypeSerializer},
    )
    def update(self, request, *args, **kwargs):
        request = m2m_array_of_str_to_url(
            request,
            ["besluittypen", "deelzaaktypen", "gerelateerde_zaaktypen"],
            self.action,
        )
        return super(viewsets.ModelViewSet, self).update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self._check_query_params(request)
        queryset = self.filter_queryset(self.get_queryset())
        filters = (
            self.filter_backends[0]()
            .get_filterset_kwargs(self.request, queryset, self)
            .get("data", {})
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer = extract_relevant_m2m(
                serializer,
                [
                    "besluittypen",
                    "informatieobjecttypen",
                    "deelzaaktypen",
                    "gerelateerde_zaaktypen",
                ],
                self.action,
                filters.get("datum_geldigheid", None),
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer = extract_relevant_m2m(
            serializer,
            [
                "besluittypen",
                "informatieobjecttypen",
                "deelzaaktypen",
                "gerelateerde_zaaktypen",
            ],
            self.action,
            filters.get("datum_geldigheid", None),
        )

        return Response(serializer.data)
