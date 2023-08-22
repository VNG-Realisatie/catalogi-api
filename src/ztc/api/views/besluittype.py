from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import BesluitType
from ..filters import BesluitTypeFilter
from ..kanalen import KANAAL_BESLUITTYPEN
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import (
    BesluitTypeCreateSerializer,
    BesluitTypeSerializer,
    BesluitTypeUpdateSerializer,
)
from ..utils.viewsets import extract_relevant_m2m, m2m_array_of_str_to_url
from .mixins import (
    ConceptMixin,
    ForcedCreateUpdateMixin,
    M2MConceptDestroyMixin,
    swagger_publish_schema,
)


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary=_("Alle BESLUITTYPEn opvragen."),
        description=_("Deze lijst kan gefilterd wordt met query-string parameters."),
    ),
    retrieve=extend_schema(
        summary=_("Een specifieke BESLUITTYPE opvragen."),
        description=_("Een specifieke BESLUITTYPE opvragen."),
    ),
    create=extend_schema(
        summary=_("Maak een BESLUITTYPE aan."),
        description=_("Maak een BESLUITTYPE aan."),
    ),
    update=extend_schema(
        summary=_("Werk een BESLUITTYPE in zijn geheel bij."),
        description=_(
            "Werk een BESLUITTYPE in zijn geheel bij. Dit kan alleen als het een concept betreft."
        ),
    ),
    partial_update=extend_schema(
        summary=_("Werk een BESLUITTYPE deels bij."),
        description=_(
            "Werk een BESLUITTYPE deels bij. Dit kan alleen als het een concept betreft."
        ),
    ),
    destroy=extend_schema(
        summary=_("Verwijder een BESLUITTYPE."),
        description=_(
            "Verwijder een BESLUITTYPE. Dit kan alleen als het een concept betreft."
        ),
    ),
    publish=extend_schema(
        summary=_("Publiceer het concept BESLUITTYPE."),
        description=_(
            "Publiceren van het besluittype zorgt ervoor dat dit in een Besluiten API kan gebruikt worden. "
            "Na het publiceren van een besluittype zijn geen inhoudelijke wijzigingen meer mogelijk. "
            "Indien er na het publiceren nog wat gewijzigd moet worden, dan moet je een nieuwe versie aanmaken."
        ),
    ),
)
class BesluitTypeViewSet(
    CheckQueryParamsMixin,
    ConceptMixin,
    M2MConceptDestroyMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    global_description = _(
        "Opvragen en bewerken van BESLUITTYPEn nodig voor BESLUITEN in de Besluiten API. "
        "Alle BESLUITTYPEn van de besluiten die het resultaat kunnen zijn van het zaakgericht werken "
        "van de behandelende organisatie(s)."
    )

    queryset = BesluitType.objects.all().order_by("-pk")
    serializer_class = BesluitTypeSerializer
    filterset_class = BesluitTypeFilter
    lookup_field = "uuid"

    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
        "publish": SCOPE_CATALOGI_WRITE,
    }
    concept_related_fields = ["informatieobjecttypen", "zaaktypen"]
    notifications_kanaal = KANAAL_BESLUITTYPEN

    @extend_schema(
        request=BesluitTypeCreateSerializer,
        responses={201: BesluitTypeSerializer},
    )
    def create(self, request, *args, **kwargs):
        request = m2m_array_of_str_to_url(
            request, ["informatieobjecttypen"], self.action
        )
        return super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)

    @extend_schema(
        request=BesluitTypeUpdateSerializer,
        responses={200: BesluitTypeSerializer},
    )
    def update(self, request, *args, **kwargs):
        request = m2m_array_of_str_to_url(
            request, ["informatieobjecttypen"], self.action
        )
        return super(viewsets.ModelViewSet, self).update(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output. Two special scenarios have been added for the retrieve and list operations. These are used to filter the m2m relations based on the geldigheid of the underlying objects.
        """
        if getattr(self, 'swagger_fake_view', False):
            return BesluitType.objects.none()

        serializer = super().get_serializer(*args, **kwargs)

        if not self.request:
            return serializer

        if self.action in ["list", "retrieve"]:
            filter_datum_geldigheid = self.request.query_params.get(
                "datumGeldigheid", None
            )

            serializer = extract_relevant_m2m(
                serializer,
                ["zaaktypen", "informatieobjecttypen", "resultaattypen"],
                self.action,
                filter_datum_geldigheid,
            )

        return serializer

    def perform_create(self, serializer):
        """automatically create new zaaktype relations when creating a new version of a besluittype"""
        new_besluittype = serializer.save()
        besluittypen = BesluitType.objects.filter(
            omschrijving=serializer.data.get("omschrijving", [])
        )
        for besluittype in besluittypen:
            for zaaktype in besluittype.zaaktypen.all():
                new_besluittype.zaaktypen.add(zaaktype)
                new_besluittype.save()


BesluitTypeViewSet.publish = swagger_publish_schema(BesluitTypeViewSet)
