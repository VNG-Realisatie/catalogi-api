from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import InformatieObjectType


class InformatieObjectTypeSerializer(NestedHyperlinkedModelSerializer):
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

            'catalogus',
            'omschrijving',
            'vertrouwelijkheidaanduiding',
            # 'omschrijvingGeneriek',
            # 'categorie',
            # 'trefwoord',
            # 'vertrouwelijkAanduiding',
            # 'model',
            # 'toelichting',
            # 'ingangsdatumObject',
            # 'einddatumObject',
            # 'isRelevantVoor',
            # 'isVastleggingVoor',
        )
