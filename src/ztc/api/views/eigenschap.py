from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ztc.datamodel.models import Eigenschap

from ..filters import EigenschapFilter
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import EigenschapSerializer
from .mixins import ForcedCreateUpdateMixin, ZaakTypeConceptMixin


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary="Alle EIGENSCHAPpen opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke EIGENSCHAP opvragen.",
        description="Een specifieke EIGENSCHAP opvragen.",
    ),
    create=extend_schema(
        summary="Maak een EIGENSCHAP aan.",
        description="Maak een EIGENSCHAP aan. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    update=extend_schema(
        summary="Werk een EIGENSCHAP in zijn geheel bij.",
        description="Werk een EIGENSCHAP in zijn geheel bij. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    partial_update=extend_schema(
        summary="Werk een EIGENSCHAP deels bij.",
        description="Werk een EIGENSCHAP deels bij. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
    destroy=extend_schema(
        summary="Verwijder een EIGENSCHAP.",
        description="Verwijder een EIGENSCHAP. Dit kan alleen als het bijbehorende ZAAKTYPE een concept betreft.",
    ),
)
class EigenschapViewSet(
    CheckQueryParamsMixin,
    ZaakTypeConceptMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):

    """
    Opvragen en bewerken van EIGENSCHAPpen van een ZAAKTYPE.

    Een relevant inhoudelijk gegeven dat bij ZAAKen van dit ZAAKTYPE geregistreerd moet kunnen worden en geen standaard kenmerk is van een zaak.
    """

    queryset = Eigenschap.objects.all().order_by("-pk")
    serializer_class = EigenschapSerializer
    filterset_class = EigenschapFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
    }
