from rest_framework import mixins, viewsets
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import RolType
from ..filters import RolTypeFilter
from ..scopes import (
    SCOPE_ZAAKTYPES_FORCED_DELETE,
    SCOPE_ZAAKTYPES_READ,
    SCOPE_ZAAKTYPES_WRITE,
)
from ..serializers import RolTypeSerializer
from .mixins import ZaakTypeConceptMixin


class RolTypeViewSet(
    CheckQueryParamsMixin, ZaakTypeConceptMixin, viewsets.ModelViewSet
):
    """
    Opvragen en bewerken van ROLTYPEn van een ZAAKTYPE.

    Generieke aanduiding van de aard van een ROL die een BETROKKENE kan
    uitoefenen in ZAAKen van een ZAAKTYPE.

    create:
    Maak een ROLTYPE aan.

    Maak een ROLTYPE aan. Dit kan alleen als het bijbehorende ZAAKTYPE een
    concept betreft.

    list:
    Alle ROLTYPEn opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke ROLTYPE opvragen.

    Een specifieke ROLTYPE opvragen.

    update:
    Werk een ROLTYPE in zijn geheel bij.

    Werk een ROLTYPE in zijn geheel bij. Dit kan alleen als het
    bijbehorende ZAAKTYPE een concept betreft.

    partial_update:
    Werk een ROLTYPE deels bij.

    Werk een ROLTYPE deels bij. Dit kan alleen als het bijbehorende
    ZAAKTYPE een concept betreft.

    destroy:
    Verwijder een ROLTYPE.

    Verwijder een ROLTYPE. Dit kan alleen als het bijbehorende ZAAKTYPE een
    concept betreft.
    """

    queryset = RolType.objects.order_by("-pk")
    serializer_class = RolTypeSerializer
    filterset_class = RolTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_ZAAKTYPES_READ,
        "retrieve": SCOPE_ZAAKTYPES_READ,
        "create": SCOPE_ZAAKTYPES_WRITE,
        "update": SCOPE_ZAAKTYPES_WRITE,
        "partial_update": SCOPE_ZAAKTYPES_WRITE,
        "destroy": SCOPE_ZAAKTYPES_WRITE | SCOPE_ZAAKTYPES_FORCED_DELETE,
    }
