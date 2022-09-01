from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.notifications.viewsets import NotificationViewSetMixin
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
from ..serializers import BesluitTypeSerializer
from .mixins import (
    ConceptMixin,
    ForcedCreateUpdateMixin,
    M2MConceptDestroyMixin,
    swagger_publish_schema,
)


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary="Alle BESLUITTYPEn opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke BESLUITTYPE opvragen.",
        description="Een specifieke BESLUITTYPE opvragen.",
    ),
    create=extend_schema(
        summary="Maak een BESLUITTYPE aan.",
        description="Maak een BESLUITTYPE aan.",
    ),
    update=extend_schema(
        summary="Werk een BESLUITTYPE in zijn geheel bij.",
        description="Werk een BESLUITTYPE in zijn geheel bij. Dit kan alleen als het een concept betreft.",
    ),
    partial_update=extend_schema(
        summary=" Werk een BESLUITTYPE deels bij.",
        description="Werk een BESLUITTYPE deels bij. Dit kan alleen als het een concept betreft.",
    ),
    destroy=extend_schema(
        summary="Verwijder een BESLUITTYPE.",
        description="Verwijder een BESLUITTYPE. Dit kan alleen als het een concept betreft.",
    ),
    publish=extend_schema(
        summary="Publiceer het concept BESLUITTYPE.",
        description="Publiceren van het besluittype zorgt ervoor dat dit in een Besluiten API kan gebruikt worden. "
        "Na het publiceren van een besluittype zijn geen inhoudelijke wijzigingen meer mogelijk. "
        "Indien er na het publiceren nog wat gewijzigd moet worden, dan moet je een nieuwe versie aanmaken.",
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
    """
    Opvragen en bewerken van BESLUITTYPEn nodig voor BESLUITEN in de Besluiten API.

    Alle BESLUITTYPEn van de besluiten die het resultaat kunnen zijn van het zaakgericht werken van de behandelende organisatie(s).
    """

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


BesluitTypeViewSet.publish = swagger_publish_schema(BesluitTypeViewSet)
