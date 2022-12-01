from typing import List

from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from drf_writable_nested import NestedCreateMixin, NestedUpdateMixin
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    SerializerMethodField,
)
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.serializers import (
    GegevensGroepSerializer,
    NestedGegevensGroepMixin,
    add_choice_values_help_text,
)
from vng_api_common.validators import ResourceValidator

from ...datamodel.choices import AardRelatieChoices, RichtingChoices
from ...datamodel.models import (
    Eigenschap,
    ResultaatType,
    RolType,
    StatusType,
    ZaakObjectType,
    ZaakType,
    ZaakTypenRelatie,
)
from ..utils.validators import RelationCatalogValidator
from ..validators import (
    ConceptUpdateValidator,
    DeelzaaktypeCatalogusValidator,
    M2MConceptCreateValidator,
    M2MConceptUpdateValidator,
    ZaaktypeGeldigheidValidator,
)
from . import (
    EigenschapSerializer,
    ResultaatTypeSerializer,
    RolTypeSerializer,
    StatusTypeSerializer,
)
from .zaakobjecttype import ZaakObjectTypeSerializer


class ReferentieProcesSerializer(GegevensGroepSerializer):
    class Meta:
        model = ZaakType
        gegevensgroep = "referentieproces"


class BronCatalogusSerializer(GegevensGroepSerializer):
    class Meta:
        model = ZaakType
        gegevensgroep = "broncatalogus"


class BronZaaktypeSerializer(GegevensGroepSerializer):
    class Meta:
        model = ZaakType
        gegevensgroep = "bronzaaktype"


class ZaakTypenRelatieSerializer(ModelSerializer):
    class Meta:
        model = ZaakTypenRelatie
        fields = ("zaaktype", "aard_relatie", "toelichting")
        extra_kwargs = {"zaaktype": {"source": "gerelateerd_zaaktype"}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(AardRelatieChoices)
        self.fields["aard_relatie"].help_text += f"\n\n{value_display_mapping}"


class HistoryURLField(SerializerMethodField):
    def __init__(self, resource, resource_serializer, method_name=None):
        super().__init__(method_name)
        self.func_args = (resource, resource_serializer)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value, *self.func_args)


class ZaakTypeSerializer(
    NestedGegevensGroepMixin,
    NestedCreateMixin,
    NestedUpdateMixin,
    HyperlinkedModelSerializer,
):

    referentieproces = ReferentieProcesSerializer(
        required=True,
        help_text=_("Het Referentieproces dat ten grondslag ligt aan dit ZAAKTYPE."),
    )
    gerelateerde_zaaktypen = ZaakTypenRelatieSerializer(
        many=True,
        source="zaaktypenrelaties",
        help_text="De ZAAKTYPEn van zaken die relevant zijn voor zaken van dit ZAAKTYPE.",
    )

    broncatalogus = BronCatalogusSerializer(
        required=False, help_text=_("De CATALOGUS waaraan het ZAAKTYPE is ontleend.")
    )

    bronzaaktype = BronZaaktypeSerializer(
        required=False,
        help_text=_(
            "Het zaaktype binnen de CATALOGUS waaraan dit ZAAKTYPE is ontleend."
        ),
    )
    roltypen = HistoryURLField(
        method_name="create_custom_urls",
        resource=RolType,
        resource_serializer=RolTypeSerializer,
    )
    statustypen = HistoryURLField(
        method_name="create_custom_urls",
        resource=StatusType,
        resource_serializer=StatusTypeSerializer,
    )
    resultaattypen = HistoryURLField(
        method_name="create_custom_urls",
        resource=ResultaatType,
        resource_serializer=ResultaatTypeSerializer,
    )
    eigenschappen = HistoryURLField(
        method_name="create_custom_urls",
        resource=Eigenschap,
        resource_serializer=EigenschapSerializer,
    )

    zaakobjecttypen = HistoryURLField(
        method_name="create_custom_urls",
        resource=ZaakObjectType,
        resource_serializer=ZaakObjectTypeSerializer,
    )

    def create_custom_urls(self, zaaktype, resource, resource_serializer) -> List[str]:

        if not zaaktype.datum_einde_geldigheid:
            valid_resources = resource.objects.filter(
                Q(datum_einde_geldigheid=zaaktype.datum_einde_geldigheid)
                & Q(zaaktype__identificatie=zaaktype.identificatie)
            )

        else:
            valid_resources = resource.objects.filter(
                Q(datum_begin_geldigheid__lte=zaaktype.datum_begin_geldigheid)
                & Q(zaaktype__identificatie=zaaktype.identificatie)
                & Q(datum_einde_geldigheid__gte=zaaktype.datum_einde_geldigheid)
                | Q(datum_einde_geldigheid=None)
                & Q(zaaktype__identificatie=zaaktype.identificatie)
                & Q(datum_begin_geldigheid__lte=zaaktype.datum_begin_geldigheid)
            )

        serializer = resource_serializer(
            valid_resources,
            many=True,
            context={"request": self.context["request"]},
        ).data

        valid_resources_urls = []
        for ordered_dict in serializer:
            valid_resources_urls.append(ordered_dict["url"])
        return valid_resources_urls

    class Meta:
        model = ZaakType
        fields = (
            "url",
            "identificatie",
            "omschrijving",
            "omschrijving_generiek",
            "vertrouwelijkheidaanduiding",
            "doel",
            "aanleiding",
            "toelichting",
            "indicatie_intern_of_extern",
            "handeling_initiator",
            "onderwerp",
            "handeling_behandelaar",
            "doorlooptijd",
            "servicenorm",
            "opschorting_en_aanhouding_mogelijk",
            "verlenging_mogelijk",
            "verlengingstermijn",
            "trefwoorden",
            "publicatie_indicatie",
            "publicatietekst",
            "verantwoordingsrelatie",
            "producten_of_diensten",
            "selectielijst_procestype",
            "referentieproces",
            "verantwoordelijke",
            "zaakobjecttypen",
            "broncatalogus",
            "bronzaaktype",
            # relaties
            "catalogus",
            "statustypen",
            "resultaattypen",
            "eigenschappen",
            "informatieobjecttypen",
            "roltypen",
            "besluittypen",
            "deelzaaktypen",
            "gerelateerde_zaaktypen",
            "begin_geldigheid",
            "einde_geldigheid",
            "begin_object",
            "einde_object",
            "versiedatum",
            "concept",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "omschrijving": {"source": "zaaktype_omschrijving"},
            "omschrijving_generiek": {"source": "zaaktype_omschrijving_generiek"},
            "catalogus": {"lookup_field": "uuid"},
            "doorlooptijd": {"source": "doorlooptijd_behandeling"},
            "servicenorm": {"source": "servicenorm_behandeling"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
            "begin_object": {"source": "datum_begin_object"},
            "einde_object": {"source": "datum_einde_object"},
            "concept": {"read_only": True},
            "producten_of_diensten": {"allow_empty": True},
            "selectielijst_procestype": {
                "validators": [
                    ResourceValidator("ProcesType", settings.REFERENTIELIJSTEN_API_SPEC)
                ]
            },
            "informatieobjecttypen": {
                "read_only": True,
                "lookup_field": "uuid",
                "help_text": _(
                    "URL-referenties naar de INFORMATIEOBJECTTYPEN die mogelijk zijn binnen dit ZAAKTYPE."
                ),
            },
            "besluittypen": {
                "label": _("heeft relevante besluittypen"),
                "lookup_field": "uuid",
            },
            "deelzaaktypen": {"lookup_field": "uuid"},
        }

        validators = [
            # ZaaktypeGeldigheidValidator(),
            RelationCatalogValidator("besluittypen"),
            ConceptUpdateValidator(),
            # M2MConceptCreateValidator(["besluittypen", "informatieobjecttypen"]),
            # M2MConceptUpdateValidator(["besluittypen", "informatieobjecttypen"]),
            DeelzaaktypeCatalogusValidator(),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value_display_mapping = add_choice_values_help_text(
            VertrouwelijkheidsAanduiding
        )
        self.fields[
            "vertrouwelijkheidaanduiding"
        ].help_text += f"\n\n{value_display_mapping}"

        value_display_mapping = add_choice_values_help_text(RichtingChoices)
        self.fields[
            "indicatie_intern_of_extern"
        ].help_text += f"\n\n{value_display_mapping}"
