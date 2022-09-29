from django.utils.translation import gettext as _

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ztc.datamodel.models import Catalogus

from ..filters import CatalogusFilter
from ..scopes import SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE
from ..serializers import CatalogusSerializer


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary=_("Alle CATALOGUSsen opvragen."),
        description=_("Deze lijst kan gefilterd wordt met query-string parameters."),
    ),
    retrieve=extend_schema(
        summary=_("Een specifieke CATALOGUS opvragen."),
        description=_("Een specifieke CATALOGUS opvragen."),
    ),
    create=extend_schema(
        summary=_("Maak een CATALOGUS aan."),
        description=_("Maak een CATALOGUS aan."),
    ),
    update=extend_schema(
        summary=_("Werk een CATALOGUS in zijn geheel bij."),
        description=_("Werk een CATALOGUS in zijn geheel bij."),
    ),
    partial_update=extend_schema(
        summary=_("Werk een CATALOGUS deels bij."),
        description=_("Werk een CATALOGUS deels bij."),
    ),
    destroy=extend_schema(
        summary=_("Verwijder een CATALOGUS."),
        description=_(
            "Verwijder een CATALOGUS. "
            "Dit kan alleen als er geen onderliggende ZAAKTYPEn, INFORMATIEOBJECTTYPEn en BESLUITTYPEn zijn."
        ),
    ),
)
class CatalogusViewSet(
    CheckQueryParamsMixin, mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet
):
    global_description = (
        "Opvragen en bewerken van CATALOGUSsen. De verzameling van ZAAKTYPEn, INFORMATIEOBJECTTYPEn en "
        "BESLUITTYPEn voor een domein die als één geheel beheerd wordt."
    )

    queryset = Catalogus.objects.all().order_by("-pk")
    serializer_class = CatalogusSerializer
    filter_class = CatalogusFilter
    lookup_field = "uuid"
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE,
    }
