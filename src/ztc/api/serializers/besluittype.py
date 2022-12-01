from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ...datamodel.models import BesluitType, InformatieObjectType, ZaakType
from ..utils.validators import RelationCatalogValidator
from ..validators import (
    ConceptUpdateValidator,
    M2MConceptCreateValidator,
    M2MConceptUpdateValidator,
)


class BesluitTypeSerializer(serializers.HyperlinkedModelSerializer):
    resultaattypen_omschrijving = serializers.SlugRelatedField(
        many=True,
        source="resultaattypen",
        read_only=True,
        slug_field="omschrijving",
        help_text=_("Omschrijving van de aard van resultaten van het RESULTAATTYPE."),
    )
    vastgelegd_in = serializers.SlugRelatedField(
        many=True,
        source="informatieobjecttypen",
        read_only=True,
        slug_field="omschrijving",
        help_text=_(
            "Omschrijving van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE."
        ),
    )

    class Meta:
        model = BesluitType
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
            "begin_object": {"source": "datum_begin_object"},
            "einde_object": {"source": "datum_einde_object"},
            "concept": {"read_only": True},
            "informatieobjecttypen": {
                "lookup_field": "uuid",
                "required": True,
                "allow_empty": True,
            },
            "zaaktypen": {"lookup_field": "uuid", "allow_empty": True},
            "resultaattypen": {
                "lookup_field": "uuid",
                "read_only": True,
                "help_text": _(
                    "Het BESLUITTYPE van besluiten die gepaard gaan met resultaten"
                    " van het RESULTAATTYPE."
                ),
            },
        }
        fields = (
            "url",
            "catalogus",
            "zaaktypen",
            "omschrijving",
            "omschrijving_generiek",
            "besluitcategorie",
            "reactietermijn",
            "publicatie_indicatie",
            "publicatietekst",
            "publicatietermijn",
            "toelichting",
            "informatieobjecttypen",
            "begin_geldigheid",
            "einde_geldigheid",
            "begin_object",
            "einde_object",
            "concept",
            "resultaattypen",
            "resultaattypen_omschrijving",
            "vastgelegd_in",
        )
        validators = [
            # UniqueTogetherValidator(
            #     queryset=BesluitType.objects.all(), fields=["catalogus", "omschrijving"]
            # ),
            RelationCatalogValidator("informatieobjecttypen"),
            RelationCatalogValidator("zaaktypen"),
            ConceptUpdateValidator(),
            # M2MConceptCreateValidator(["zaaktypen", "informatieobjecttypen"]),
            # M2MConceptUpdateValidator(["zaaktypen", "informatieobjecttypen"]),
        ]
