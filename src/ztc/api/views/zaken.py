from django.utils.translation import ugettext_lazy as _

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings
from vng_api_common.caching import conditional_retrieve
from vng_api_common.inspectors.view import COMMON_ERRORS
from vng_api_common.notifications.viewsets import NotificationViewSetMixin
from vng_api_common.serializers import FoutSerializer, ValidatieFoutSerializer
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import ZaakType
from ...datamodel.utils import set_geldigheid, set_geldigheid_nestled_resources
from ..filters import ZaakTypeFilter
from ..kanalen import KANAAL_ZAAKTYPEN
from ..scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..serializers import ZaakTypeSerializer
from .mixins import ConceptMixin, M2MConceptDestroyMixin


@conditional_retrieve()
class ZaakTypeViewSet(
    CheckQueryParamsMixin,
    ConceptMixin,
    M2MConceptDestroyMixin,
    NotificationViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    Opvragen en bewerken van ZAAKTYPEn nodig voor ZAKEN in de Zaken API.

    Een ZAAKTYPE beschrijft het geheel van karakteristieke eigenschappen van
    zaken van eenzelfde soort.

    create:
    Maak een ZAAKTYPE aan.

    Maak een ZAAKTYPE aan.

    Er wordt gevalideerd op:
    - geldigheid `catalogus` URL, dit moet een catalogus binnen dezelfde API zijn
    - Uniciteit `catalogus` en `omschrijving`. Dezelfde omeschrijving mag enkel
      opnieuw gebruikt worden als het zaaktype een andere geldigheidsperiode
      kent dan bestaande zaaktypen.
    - `deelzaaktypen` moeten tot dezelfde catalogus behoren als het ZAAKTYPE.

    list:
    Alle ZAAKTYPEn opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke ZAAKTYPE opvragen.

    Een specifieke ZAAKTYPE opvragen.

    update:
    Werk een ZAAKTYPE in zijn geheel bij.

    Werk een ZAAKTYPE in zijn geheel bij. Dit kan alleen als het een concept
    betreft.

    Er wordt gevalideerd op:
    - `deelzaaktypen` moeten tot dezelfde catalogus behoren als het ZAAKTYPE.

    partial_update:
    Werk een ZAAKTYPE deels bij.

    Werk een ZAAKTYPE deels bij. Dit kan alleen als het een concept betreft.

    Er wordt gevalideerd op:
    - `deelzaaktypen` moeten tot dezelfde catalogus behoren als het ZAAKTYPE.

    destroy:
    Verwijder een ZAAKTYPE.

    Verwijder een ZAAKTYPE. Dit kan alleen als het een concept betreft.
    """

    queryset = ZaakType.objects.prefetch_related(
        "statustypen",
        "zaaktypenrelaties",
        "informatieobjecttypen",
        "statustypen",
        "resultaattypen",
        "eigenschap_set",
        "roltype_set",
        "besluittypen",
        "objecttypen",
    ).order_by("-pk")
    serializer_class = ZaakTypeSerializer
    lookup_field = "uuid"
    filterset_class = ZaakTypeFilter
    required_scopes = {
        "list": SCOPE_CATALOGI_READ,
        "retrieve": SCOPE_CATALOGI_READ,
        "create": SCOPE_CATALOGI_WRITE,
        "update": SCOPE_CATALOGI_WRITE,
        "partial_update": SCOPE_CATALOGI_WRITE,
        "destroy": SCOPE_CATALOGI_WRITE | SCOPE_CATALOGI_FORCED_DELETE,
        "publish": SCOPE_CATALOGI_WRITE,
    }
    concept_related_fields = ["besluittypen", "informatieobjecttypen"]
    notifications_kanaal = KANAAL_ZAAKTYPEN
    relation_fields = ["zaaktypenrelaties"]

    @swagger_auto_schema(
        request_body=no_body,
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: ValidatieFoutSerializer,
            status.HTTP_404_NOT_FOUND: FoutSerializer,
            **{exc.status_code: FoutSerializer for exc in COMMON_ERRORS},
        },
    )
    @action(detail=True, methods=["post"])
    def publish(self, request, *args, **kwargs):
        """
        Publiceer het concept ZAAKTYPE.

        Publiceren van het zaaktype zorgt ervoor dat dit in een Zaken API kan gebruikt
        worden. Na het publiceren van een zaaktype zijn geen inhoudelijke wijzigingen
        meer mogelijk - ook niet de statustypen, eigenschappen... etc. Indien er na het
        publiceren nog wat gewijzigd moet worden, dan moet je een nieuwe versie
        aanmaken.
        """
        instance = self.get_object()
        # check related objects
        if (
            instance.besluittypen.filter(concept=True).exists()
            or instance.informatieobjecttypen.filter(concept=True).exists()
            or instance.deelzaaktypen.filter(concept=True).exists()
        ):
            msg = _("All related resources should be published")
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: msg}, code="concept-relation"
            )

        set_geldigheid_nestled_resources(instance)
        instance = set_geldigheid(instance)
        instance.concept = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)
