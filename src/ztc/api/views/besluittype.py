import uuid

from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from rest_framework.response import Response
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import BesluitType, ZaakType
from ..filters import BesluitTypeFilter
from ..kanalen import KANAAL_BESLUITTYPEN
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import BesluitTypeSerializer
from ..utils.viewsets import build_absolute_url, is_url
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
    NotificationViewSetMixin,
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

    def create(self, request, *args, **kwargs):
        request = self.zaaktypen_identificaties_to_urls(request)
        return super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request = self.zaaktypen_identificaties_to_urls(request)
        return super(viewsets.ModelViewSet, self).update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        return only the most recent object based on 'datum_geldigheid' and 'concept=False'
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        zaaktypen = serializer.data["zaaktypen"]

        for i, url in enumerate(zaaktypen):
            uuid_from_url = uuid.UUID(url.rsplit("/", 1)[1]).hex
            valid_zaak = ZaakType.objects.filter(
                uuid=uuid_from_url, concept=False, datum_einde_geldigheid=None
            )
            if not valid_zaak:
                serializer.data["zaaktypen"].pop(i)

        return Response(serializer.data)

    def zaaktypen_identificaties_to_urls(self, request):
        """
        The array of 'zaaktypen_identificaties' is transformed to an array of urls, which are required for the
        m2m relationship. The corresponding urls are based on their most recent 'geldigheid' date, denoted by 'datum_einde_geldigheid=None'.
        """
        urls = []
        for identificatie in request.data.get("zaaktypen", []):
            if is_url(identificatie):
                return request

            zaaktypen = ZaakType.objects.filter(
                identificatie=identificatie, datum_einde_geldigheid=None
            )
            for zaaktype in zaaktypen:
                urls.append(
                    f"{build_absolute_url(self.action, request)}/zaaktypen/{str(zaaktype.uuid)}"
                )
        request.data["zaaktypen"] = urls
        return request

    def get_object(self):
        """
        return only the most recent object based on 'datum_geldigheid' and 'concept=False'
        """
        obj = super(BesluitTypeViewSet, self).get_object()
        most_recent_zaaktype = obj.zaaktypen.filter(
            datum_einde_geldigheid=None, concept=False
        )
        if most_recent_zaaktype:
            obj.zaaktypen.set(most_recent_zaaktype)
        return obj


BesluitTypeViewSet.publish = swagger_publish_schema(BesluitTypeViewSet)
