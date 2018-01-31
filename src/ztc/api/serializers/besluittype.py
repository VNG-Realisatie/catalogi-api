from rest_framework import serializers

from ...datamodel.models import BesluitType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin

class BesluitTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializer based on ``BST-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """

    class Meta:
        model = BesluitType
        source_mapping = {
            'omschrijving': 'besluittype_omschrijving',
            'omschrijvingGeneriek': 'besluittype_omschrijving_generiek',
            'categorie': 'besluitcategorie',
            'publicatieIndicatie': 'publicatie_indicatie',
            'publicatieTekst': 'publicatietekst',
            'publicatieTermijn': 'publicatietermijn',
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',

            'maaktDeeluitVan': 'maakt_deel_uit_van',
            'wordtVastgelegdIn': 'wordt_vastgelegd_in',

            # 'isRelevantVoor': '',
            # 'isResultaatVan': '',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:informatieobjecttype-detail'},
            'maaktDeeluitVan': {'view_name': 'api:catalogus-detail'},
            'wordtVastgelegdIn': {'view_name': 'api:informatieobjecttype-detail'},
        }
        fields = (
            'omschrijving',
            'omschrijvingGeneriek',
            'categorie',
            'reactietermijn',
            'publicatieIndicatie',
            'publicatieTekst',
            'publicatieTermijn',
            'toelichting',

            'maaktDeeluitVan',
            'wordtVastgelegdIn',

            # 'isRelevantVoor',
            # 'isResultaatVan',
        )
