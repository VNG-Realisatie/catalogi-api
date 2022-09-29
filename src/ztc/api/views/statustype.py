from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import StatusType
from ..filters import StatusTypeFilter
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import StatusTypeSerializer
from .mixins import ForcedCreateUpdateMixin, ZaakTypeConceptMixin


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary=_("Alle STATUSTYPEn opvragen."),
        description=_("Deze lijst kan gefilterd wordt met query-string parameters."),
    ),
    retrieve=extend_schema(
        summary=_("Een specifieke STATUSTYPE opvragen."),
        description=_("Een specifieke STATUSTYPE opvragen."),
    ),
    create=extend_schema(
        summary=_("Maak een STATUSTYPE aan."),
        description=_(
            "Maak een STATUSTYPE aan. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft."
        ),
    ),
    update=extend_schema(
        summary=_("Werk een STATUSTYPE in zijn geheel bij."),
        description=_(
            "Werk een STATUSTYPE in zijn geheel bij. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft."
        ),
    ),
    partial_update=extend_schema(
        summary=_("Werk een STATUSTYPE deels bij."),
        description=_(
            "Werk een STATUSTYPE deels bij. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft."
        ),
    ),
    destroy=extend_schema(
        summary=_("Verwijder een STATUSTYPE."),
        description=_(
            "Verwijder een STATUSTYPE. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft."
        ),
    ),
)
class StatusTypeViewSet(
    CheckQueryParamsMixin,
    ZaakTypeConceptMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    global_description = (
        "Opvragen en bewerken van STATUSTYPEn van een ZAAKTYPE. "
        "Generieke aanduiding van de aard van een status."
    )

    queryset = StatusType.objects.all().order_by("-pk")
    serializer_class = StatusTypeSerializer
    filterset_class = StatusTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
    }
