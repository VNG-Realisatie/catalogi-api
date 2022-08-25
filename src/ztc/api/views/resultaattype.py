from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import ResultaatType
from ..filters import ResultaatTypeFilter
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import ResultaatTypeSerializer
from .mixins import ForcedCreateUpdateMixin, ZaakTypeConceptMixin


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary="Alle RESULTAATTYPEn opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke RESULTAATTYPE opvragen.",
        description="Een specifieke RESULTAATTYPE opvragen.",
    ),
    create=extend_schema(
        summary="Maak een RESULTAATTYPE aan.",
        description="Maak een RESULTAATTYPE aan. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    update=extend_schema(
        summary="Werk een RESULTAATTYPE in zijn geheel bij.",
        description="Werk een RESULTAATTYPE in zijn geheel bij. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    partial_update=extend_schema(
        summary="Werk een RESULTAATTYPE deels bij.",
        description="Werk een RESULTAATTYPE deels bij. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    destroy=extend_schema(
        summary="Verwijder een RESULTAATTYPE.",
        description="Verwijder een RESULTAATTYPE. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
)
class ResultaatTypeViewSet(
    CheckQueryParamsMixin,
    ZaakTypeConceptMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    """
    Opvragen en bewerken van RESULTAATTYPEn van een ZAAKTYPE.

    Het betreft de indeling of groepering van resultaten van zaken van hetzelfde ZAAKTYPE naar hun aard, zoals 'verleend', 'geweigerd', 'verwerkt', etc.
    """

    queryset = ResultaatType.objects.all().order_by("-pk")
    serializer_class = ResultaatTypeSerializer
    filter_class = ResultaatTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
    }
