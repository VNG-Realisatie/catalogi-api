from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import RolType
from ..filters import RolTypeFilter
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import RolTypeSerializer
from .mixins import ForcedCreateUpdateMixin, ZaakTypeConceptMixin


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary="Alle ROLTYPEn opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke ROLTYPE opvragen.",
        description="Een specifieke ROLTYPE opvragen.",
    ),
    create=extend_schema(
        summary="Maak een ROLTYPE aan.",
        description="Maak een ROLTYPE aan. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    update=extend_schema(
        summary="Werk een ROLTYPE in zijn geheel bij.",
        description="Werk een ROLTYPE in zijn geheel bij. Dit kan alleen als het een concept betreft.",
    ),
    partial_update=extend_schema(
        summary="Werk een ROLTYPE deels bij.",
        description="Werk een ROLTYPE deels bij. Dit kan alleen als het een concept betreft.",
    ),
    destroy=extend_schema(
        summary="Verwijder een ROLTYPE.",
        description="Verwijder een ROLTYPE. Dit kan alleen als het een concept betreft.",
    ),
)
class RolTypeViewSet(
    CheckQueryParamsMixin,
    ZaakTypeConceptMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    """
    Opvragen en bewerken van ROLTYPEn van een ZAAKTYPE.

    Generieke aanduiding van de aard van een ROL die een BETROKKENE kan uitoefenen in ZAAKen van een ZAAKTYPE.
    """

    queryset = RolType.objects.order_by("-pk")
    serializer_class = RolTypeSerializer
    filterset_class = RolTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
    }
