from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from vng_api_common.utils import get_help_text

from ...datamodel.models import BesluitType, InformatieObjectType, ZaakType
from ..utils.validators import RelationCatalogValidator
from ..validators import (
    ConceptUpdateValidator,
    M2MConceptCreateValidator,
    M2MConceptUpdateValidator,
)


class BesluitTypeSerializer(serializers.HyperlinkedModelSerializer):
    informatieobjecttypen = serializers.HyperlinkedRelatedField(
        view_name="informatieobjecttype-detail",
        many=True,
        lookup_field="uuid",
        queryset=InformatieObjectType.objects.all(),
        help_text=get_help_text("datamodel.BesluitType", "informatieobjecttypen"),
    )

    zaaktypes = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="zaaktype-detail",
        lookup_field="uuid",
        queryset=ZaakType.objects.all(),
        help_text=get_help_text("datamodel.BesluitType", "zaaktypes"),
    )

    class Meta:
        model = BesluitType
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "catalogus": {"lookup_field": "uuid"},
            "begin_geldigheid": {"source": "datum_begin_geldigheid"},
            "einde_geldigheid": {"source": "datum_einde_geldigheid"},
            "concept": {"read_only": True},
        }
        fields = (
            "url",
            "catalogus",
            "zaaktypes",
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
            RelationCatalogValidator("zaaktypes"),
            ConceptUpdateValidator(),
            M2MConceptCreateValidator(["zaaktypes", "informatieobjecttypen"]),
            M2MConceptUpdateValidator(["zaaktypes", "informatieobjecttypen"]),
        ]
