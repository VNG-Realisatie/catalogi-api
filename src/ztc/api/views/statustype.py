from rest_framework import mixins, viewsets
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import StatusType
from ..filters import StatusTypeFilter
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import StatusTypeSerializer
from .mixins import ZaakTypeConceptMixin


class StatusTypeViewSet(
    CheckQueryParamsMixin, ZaakTypeConceptMixin, viewsets.ModelViewSet
):
    """
    Opvragen en bewerken van STATUSTYPEn van een ZAAKTYPE.

    Generieke aanduiding van de aard van een status.

    create:
    Maak een STATUSTYPE aan.

    Maak een STATUSTYPE aan. Dit kan alleen als het bijbehorende ZAAKTYPE een
    concept betreft.

    list:
    Alle STATUSTYPEn opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke STATUSTYPE opvragen.

    Een specifieke STATUSTYPE opvragen.

    update:
    Werk een STATUSTYPE in zijn geheel bij.

    Werk een STATUSTYPE in zijn geheel bij. Dit kan alleen als het
    bijbehorende ZAAKTYPE een concept betreft.

    partial_update:
    Werk een STATUSTYPE deels bij.

    Werk een STATUSTYPE deels bij. Dit kan alleen als het bijbehorende
    ZAAKTYPE een concept betreft.

    destroy:
    Verwijder een STATUSTYPE.

    Verwijder een STATUSTYPE. Dit kan alleen als het bijbehorende ZAAKTYPE een
    concept betreft.
    """

    queryset = StatusType.objects.all().order_by("-pk")
    serializer_class = StatusTypeSerializer
    filterset_class = StatusTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE,
        "update": SCOPE_CATALOGI_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
    }
