from django.utils.translation import gettext as _

from rest_framework import serializers
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.serializers import add_choice_values_help_text

from ...datamodel.models import (
    InformatieObjectType,
    InformatieObjectTypeOmschrijvingGeneriek,
)
from ..validators import ConceptUpdateValidator


class InformatieObjectTypeOmschrijvingGeneriekSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformatieObjectTypeOmschrijvingGeneriek
        fields = (
            "informatieobjecttype_omschrijving_generiek",
            "definitie_informatieobjecttype_omschrijving_generiek",
            "herkomst_informatieobjecttype_omschrijving_generiek",
            "hierarchie_informatieobjecttype_omschrijving_generiek",
            "opmerking_informatieobjecttype_omschrijving_generiek",
        )


class InformatieObjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer based on ``IOT-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """

    omschrijving_generiek = InformatieObjectTypeOmschrijvingGeneriekSerializer(
        required=False
    )

    class Meta:
        model = InformatieObjectType
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
            "begin_object": {"source": "datum_begin_object"},
            "einde_object": {"source": "datum_einde_object"},
            "concept": {"read_only": True},
            "zaaktypen": {
                "lookup_field": "uuid",
                "read_only": True,
                "help_text": _(
                    "URL-referenties naar De INFORMATIEOBJECTTYPEn die relevant"
                    " kunnen zijn voor ZAAKen van dit ZAAKTYPE."
                ),
            },
            "besluittypen": {
                "lookup_field": "uuid",
                "read_only": True,
                "help_text": _(
                    "URL-referenties naar het INFORMATIEOBJECTTYPE van informatieobjecten"
                    " waarin besluiten van dit BESLUITTYPE worden vastgelegd."
                ),
            },
        }
        fields = (
            "url",
            "catalogus",
            "omschrijving",
            "vertrouwelijkheidaanduiding",
            "begin_geldigheid",
            "einde_geldigheid",
            "begin_object",
            "einde_object",
            "concept",
            "zaaktypen",
            "besluittypen",
            "informatieobjectcategorie",
            "trefwoord",
            "omschrijving_generiek",
        )
        validators = [
            ConceptUpdateValidator(),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(
            VertrouwelijkheidsAanduiding
        )
        self.fields[
            "vertrouwelijkheidaanduiding"
        ].help_text += f"\n\n{value_display_mapping}"
