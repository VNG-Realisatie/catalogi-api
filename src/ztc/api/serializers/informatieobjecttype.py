from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import InformatieObjectType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class InformatieObjectTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    """
    Serializer based on ``IOT-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """
    parent_lookup_kwargs = {
        'catalogus_pk': 'maakt_deel_uit_van__pk'
    }

    omschrijvingGeneriek = serializers.CharField(
        source='informatieobjecttype_omschrijving_generiek.informatieobjecttype_omschrijving_generiek')

    isVastleggingVoor = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van_id'}
    )
    isRelevantVoor = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaakinformatieobjecttype_set',
        view_name='api:iotzkt-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'informatieobjecttype_pk': 'informatie_object_type__pk',
        }
    )

    class Meta:
        model = InformatieObjectType
        source_mapping = {
            'omschrijving': 'informatieobjecttype_omschrijving',
            'categorie': 'informatieobjectcategorie',
            'trefwoord': 'informatieobjecttypetrefwoord',
            'vertrouwelijkAanduiding': 'vertrouwelijkheidaanduiding',
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',

            'maaktDeeluitVan': 'maakt_deel_uit_van',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:informatieobjecttype-detail'},
            'maaktDeeluitVan': {'view_name': 'api:catalogus-detail'},
        }
        fields = (
            'url',

            'omschrijving',
            'omschrijvingGeneriek',
            'categorie',
            'trefwoord',
            'vertrouwelijkAanduiding',
            'model',
            'toelichting',
            'ingangsdatumObject',
            'einddatumObject',
            'maaktDeeluitVan',
            'isRelevantVoor',
            'isVastleggingVoor',
        )

    expandable_fields = {
        'maaktDeeluitVan': ('ztc.api.serializers.CatalogusSerializer', {'source': 'maakt_deel_uit_van'}),
        'isRelevantVoor': ('ztc.api.serializers.InformatieObjectTypeZaakTypeSerializer', {'source': 'zaakinformatieobjecttype_set'}),
        'isVastleggingVoor': ('ztc.api.serializers.BesluitTypeSerializer', {'source': 'besluittype_set', 'many': True})
    }
