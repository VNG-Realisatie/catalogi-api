from django.forms import model_to_dict
from django.utils.translation import gettext as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from notifications_api_common.viewsets import NotificationViewSetMixin
from rest_framework import viewsets
from vng_api_common.caching import conditional_retrieve
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import InformatieObjectType, ZaakInformatieobjectType
from ..filters import InformatieObjectTypeFilter
from ..kanalen import KANAAL_INFORMATIEOBJECTTYPEN
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import InformatieObjectTypeSerializer
from .mixins import (
    ConceptMixin,
    ForcedCreateUpdateMixin,
    M2MConceptDestroyMixin,
    swagger_publish_schema,
)


@conditional_retrieve()
@extend_schema_view(
    list=extend_schema(
        summary=_("Alle INFORMATIEOBJECTTYPEn opvragen."),
        description=_("Deze lijst kan gefilterd wordt met query-string parameters."),
    ),
    retrieve=extend_schema(
        summary=_("Een specifieke INFORMATIEOBJECTTYPE opvragen."),
        description=_("Een specifieke INFORMATIEOBJECTTYPE opvragen."),
    ),
    create=extend_schema(
        summary=_("Maak een INFORMATIEOBJECTTYPE aan."),
        description=_("Maak een INFORMATIEOBJECTTYPE aan."),
    ),
    update=extend_schema(
        summary=_("Werk een INFORMATIEOBJECTTYPE in zijn geheel bij."),
        description=_(
            "Werk een INFORMATIEOBJECTTYPE in zijn geheel bij. Dit kan alleen als het een concept betreft."
        ),
    ),
    partial_update=extend_schema(
        summary=_("     Werk een INFORMATIEOBJECTTYPE deels bij."),
        description=_(
            "Werk een INFORMATIEOBJECTTYPE deels bij. Dit kan alleen als het een concept betreft."
        ),
    ),
    destroy=extend_schema(
        summary=_("Verwijder een INFORMATIEOBJECTTYPE."),
        description=_(
            "Verwijder een INFORMATIEOBJECTTYPE. Dit kan alleen als het een concept betreft."
        ),
    ),
    publish=extend_schema(
        summary=_("Publiceer het concept INFORMATIEOBJECTTYPE."),
        description=_(
            "Publiceren van het informatieobjecttype zorgt ervoor dat dit in een Documenten API kan gebruikt worden."
            " Na het publiceren van een informatieobjecttype zijn geen inhoudelijke wijzigingen meer mogelijk. "
            "Indien er na het publiceren nog wat gewijzigd moet worden, dan moet je een nieuwe versie aanmaken."
        ),
    ),
)
class InformatieObjectTypeViewSet(
    CheckQueryParamsMixin,
    ConceptMixin,
    M2MConceptDestroyMixin,
    NotificationViewSetMixin,
    ForcedCreateUpdateMixin,
    viewsets.ModelViewSet,
):
    global_description = (
        "Opvragen en bewerken van INFORMATIEOBJECTTYPEn nodig voor INFORMATIEOBJECTen in de Documenten "
        "API. Een INFORMATIEOBJECTTYPE beschijft de karakteristieken van een document of ander object"
        " dat informatie bevat."
    )

    queryset = InformatieObjectType.objects.all().order_by("-pk")
    serializer_class = InformatieObjectTypeSerializer
    filterset_class = InformatieObjectTypeFilter
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
    concept_related_fields = ["besluittypen", "zaaktypen"]
    notifications_kanaal = KANAAL_INFORMATIEOBJECTTYPEN

    def perform_create(self, serializer):
        """Automatically create new ZaakInformatieobjectType relation on POST"""

        informatieobjecttype = serializer.save()
        associated_ziot = ZaakInformatieobjectType.objects.filter(
            informatieobjecttype__omschrijving=informatieobjecttype.omschrijving,
            informatieobjecttype__datum_einde_geldigheid=None,
            informatieobjecttype__concept=False,
        ).get()
        kwargs = model_to_dict(
            associated_ziot, exclude=["uuid", "id", "zaaktype", "informatieobjecttype"]
        )

        ZaakInformatieobjectType.objects.create(
            **kwargs,
            informatieobjecttype=informatieobjecttype,
            zaaktype=associated_ziot.zaaktype
        )


InformatieObjectTypeViewSet.publish = swagger_publish_schema(
    InformatieObjectTypeViewSet
)
