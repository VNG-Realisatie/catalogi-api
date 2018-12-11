from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import InformatieObjectType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class InformatieObjectTypeSerializer(SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    """
    Serializer based on ``IOT-basis`` specified in XSD ``ztc0310_ent_basis.xsd``.
    """
    parent_lookup_kwargs = {
        'catalogus_uuid': 'catalogus__uuid',
    }

    # This is needed because spanning relations is not done correctly when specifying the ``source`` attribute later,
    # as is done by the ``Meta.source_mapping`` property.
    # omschrijvingGeneriek = serializers.CharField(
    #     read_only=True,
    #     source='informatieobjecttype_omschrijving_generiek.informatieobjecttype_omschrijving_generiek',
    #     max_length=80,
    #     help_text=_('Algemeen gehanteerde omschrijving van het type informatieobject.')
    # )
    #
    # isVastleggingVoor = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='besluittype_set',
    #     view_name='api:besluittype-detail',
    #     parent_lookup_kwargs={'catalogus_pk': 'catalogus__pk'}
    # )
    # isRelevantVoor = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='zaakinformatieobjecttype_set',
    #     view_name='api:zktiot-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'zaaktype__catalogus__pk',
    #         'zaaktype_pk': 'zaaktype__pk',
    #     }
    # )

    class Meta:
        model = InformatieObjectType
        source_mapping = {
            'omschrijving': 'informatieobjecttype_omschrijving',
            # 'categorie': 'informatieobjectcategorie',
            # 'trefwoord': 'informatieobjecttypetrefwoord',
            # 'vertrouwelijkAanduiding': 'vertrouwelijkheidaanduiding',
            # 'ingangsdatumObject': 'datum_begin_geldigheid',
            # 'einddatumObject': 'datum_einde_geldigheid',
        }
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'catalogus': {
                'lookup_field': 'uuid',
            },
        }
        fields = (
            'url',

            'omschrijving',
            # 'omschrijvingGeneriek',
            # 'categorie',
            # 'trefwoord',
            # 'vertrouwelijkAanduiding',
            # 'model',
            # 'toelichting',
            # 'ingangsdatumObject',
            # 'einddatumObject',
            'catalogus',
            # 'isRelevantVoor',
            # 'isVastleggingVoor',
        )

    # expandable_fields = {
    #     'catalogus': ('ztc.api.serializers.CatalogusSerializer', {'source': 'catalogus'}),
    #     'isRelevantVoor': ('ztc.api.serializers.InformatieObjectTypeZaakTypeSerializer', {'source': 'zaakinformatieobjecttype_set'}),
    #     'isVastleggingVoor': ('ztc.api.serializers.BesluitTypeSerializer', {'source': 'besluittype_set', 'many': True})
    # }
