from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from vng_api_common.notifications.viewsets import NotificationViewSetMixin
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import ZaakType
from ..filters import ZaakTypeFilter
from ..kanalen import KANAAL_ZAAKTYPEN
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import ZaakTypeSerializer
from .mixins import ConceptMixin, M2MConceptDestroyMixin
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

# class ZaakObjectTypeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin,
#                             FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
#     """
#     retrieve:
#     De objecttypen van objecten waarop een zaak van het ZAAKTYPE betrekking kan hebben.
#
#     list:
#     Een verzameling van ZAAKOBJECTTYPEn.
#     """
#     queryset = ZaakObjectType.objects.all()
#     serializer_class = ZaakObjectTypeSerializer
#
#     required_scopes = {
#         'list': SCOPE_ZAAKTYPES_READ,
#         'retrieve': SCOPE_ZAAKTYPES_READ,
#
#     }


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

    partial_update:
    Werk een ZAAKTYPE deels bij.

    Werk een ZAAKTYPE deels bij. Dit kan alleen als het een concept betreft.

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
    ).order_by("-pk")
    serializer_class = ZaakTypeSerializer
    lookup_field = "uuid"
    filterset_class = ZaakTypeFilter
    required_scopes = {
        "list": SCOPE_ZAAKTYPES_READ,
        "retrieve": SCOPE_ZAAKTYPES_READ,
        "create": SCOPE_ZAAKTYPES_WRITE,
        "update": SCOPE_ZAAKTYPES_WRITE,
        "partial_update": SCOPE_ZAAKTYPES_WRITE,
        "destroy": SCOPE_ZAAKTYPES_WRITE,
        "publish": SCOPE_ZAAKTYPES_WRITE,
    }
    concept_related_fields = ["besluittypen", "informatieobjecttypen"]
    notifications_kanaal = KANAAL_ZAAKTYPEN
    relation_fields = ["zaaktypenrelaties"]

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"])
    def publish(self, request, *args, **kwargs):
        instance = self.get_object()

        # check related objects
        besluittypen = instance.besluittypen.all()
        informatieobjecttypen = instance.informatieobjecttypen.all()

        for types in [besluittypen, informatieobjecttypen]:
            for relative_type in types:
                if relative_type.concept:
                    msg = _("All related resources should be published")
                    raise PermissionDenied(detail=msg)

        instance.concept = False
        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer):
        for field_name in self.relation_fields:
            field = serializer.validated_data.get(field_name, [])
            for related_object in field:
                # TODO fix url lookup to check if concept
                if not related_object["gerelateerd_zaaktype"]:
                    msg = _(
                        f"Relations to non-concept {field_name} object can't be created"
                    )
                    raise PermissionDenied(detail=msg)

        super().perform_create(serializer)

    def perform_update(self, instance):
        for field_name in self.relation_fields:
            field = getattr(self.get_object(), field_name)
            # TODO fix url lookup to check if concept
            related_non_concepts = field.filter(zaaktype__concept=False)
            if related_non_concepts.exists():
                msg = _(f"Objects related to non-concept {field_name} can't be updated")
                raise PermissionDenied(detail=msg)

        super().perform_update(instance)

    def perform_destroy(self, instance):
        for field_name in self.relation_fields:
            field = getattr(instance, field_name)
            # TODO fix url lookup to check if concept
            related_non_concepts = field.filter(zaaktype__concept=False)
            if related_non_concepts.exists():
                msg = _(
                    f"Objects related to non-concept {field_name} can't be destroyed"
                )
                raise PermissionDenied(detail=msg)

        super().perform_destroy(instance)
