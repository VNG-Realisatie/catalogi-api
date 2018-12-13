from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import MogelijkeBetrokkene, RolType


class MogelijkeBetrokkeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MogelijkeBetrokkene
        fields = (
            'betrokkene',
            'betrokkene_type',
        )


class RolTypeSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_uuid': 'zaaktype__uuid',
        'catalogus_uuid': 'zaaktype__catalogus__uuid',
    }
    zaaktype = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        },
    )

    mogelijke_betrokkenen = MogelijkeBetrokkeneSerializer(many=True, source='mogelijkebetrokkene_set')
    # magZetten = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='mag_zetten',
    #     view_name='api:statustype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_uuid': 'zaaktype__catalogus__uuid',
    #         'zaaktype_uuid': 'zaaktype__uuid',
    #     },
    # )

    class Meta:
        model = RolType
        fields = (
            'url',
            'zaaktype',
            'omschrijving',
            'omschrijving_generiek',
            'mogelijke_betrokkenen',

            # 'ingangsdatumObject',
            # 'einddatumObject',
            # 'soortBetrokkene',
            # 'magZetten',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
        }
