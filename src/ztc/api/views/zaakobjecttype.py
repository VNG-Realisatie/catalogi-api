from rest_framework import viewsets
from vng_api_common.caching.decorators import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ztc.api.filters import ZaakObjectTypeFilter
from ztc.api.serializers.zaakobjecttype import ZaakObjectTypeSerializer
from ztc.datamodel.models import ZaakObjectType

from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from . import ForcedCreateUpdateMixin


@conditional_retrieve()
class ZaakObjectTypeViewSet(
    CheckQueryParamsMixin, ForcedCreateUpdateMixin, viewsets.ModelViewSet
):
    """
    Opvragen en bewerken van ZAAKOBJECTTYPEn.

    Er wordt gevalideerd op:
    - `zaaktype` behoort tot dezelfde `catalogus`

    create:
    Maak een ZAAKOBJECTTYPE aan.

    Maak een ZAAKOBJECTTYPE aan.

    list:
    Alle ZAAKOBJECTTYPEn opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke ZAAKOBJECTTYPE opvragen.

    Een specifieke ZAAKOBJECTTYPE opvragen.

    update:
    Werk een ZAAKOBJECTTYPE in zijn geheel bij.

    Werk een ZAAKOBJECTTYPE in zijn geheel bij.

    partial_update:
    Werk een ZAAKOBJECTTYPE deels bij.

    Werk een ZAAKOBJECTTYPE deels bij.

    destroy:
    Verwijder een ZAAKOBJECTTYPE.

    Verwijder een ZAAKOBJECTTYPE.
    """

    queryset = ZaakObjectType.objects.select_related(
        "zaaktype",
        "catalogus",
    ).prefetch_related(
        "resultaattypen",
        "statustypen",
    )
    serializer_class = ZaakObjectTypeSerializer
    filterset_class = ZaakObjectTypeFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
        "publish": SCOPE_CATALOGI_WRITE,
    }
