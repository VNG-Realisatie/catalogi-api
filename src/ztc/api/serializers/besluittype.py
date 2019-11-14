from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ...datamodel.models import BesluitType
from ..utils.validators import RelationCatalogValidator
from ..validators import (
    ConceptUpdateValidator,
    M2MConceptCreateValidator,
    M2MConceptUpdateValidator,
)


class BesluitTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BesluitType
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
            "concept": {"read_only": True},
            "informatieobjecttypen": {
                "lookup_field": "uuid",
                "required": True,
                "allow_empty": True,
            },
            "zaaktypen": {"lookup_field": "uuid", "allow_empty": True},
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
            "concept",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=BesluitType.objects.all(), fields=["catalogus", "omschrijving"]
            ),
            RelationCatalogValidator("informatieobjecttypen"),
            RelationCatalogValidator("zaaktypen"),
            ConceptUpdateValidator(),
            M2MConceptCreateValidator(["zaaktypen", "informatieobjecttypen"]),
            M2MConceptUpdateValidator(["zaaktypen", "informatieobjecttypen"]),
        ]
