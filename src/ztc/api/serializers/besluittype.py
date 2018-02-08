from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import BesluitType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class BesluitTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    """
    Serializer based on ``BST-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """
    parent_lookup_kwargs = {
        'catalogus_pk': 'maakt_deel_uit_van__pk'
    }

    wordtVastgelegdIn = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='wordt_vastgelegd_in',
        view_name='api:informatieobjecttype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van_id'}
    )

    class Meta:
        model = BesluitType
        ref_name = model.__name__
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
        }
        extra_kwargs = {
            'url': {'view_name': 'api:besluittype-detail'},
            'maaktDeeluitVan': {'view_name': 'api:catalogus-detail'},
        }
        fields = (
            'url',

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

    expandable_fields = {
        'maaktDeeluitVan': ('ztc.api.serializers.CatalogusSerializer', {'source': 'maakt_deel_uit_van'}),
        'wordtVastgelegdIn': ('ztc.api.serializers.InformatieObjectTypeSerializer', {'source': 'wordt_vastgelegd_in', 'many': True})
    }
