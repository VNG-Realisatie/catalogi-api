from rest_framework.serializers import ModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import CheckListItem, StatusType
from ..utils.serializers import SourceMappingSerializerMixin


class CheckListItemSerializer(SourceMappingSerializerMixin, ModelSerializer):
    class Meta:
        model = CheckListItem
        ref_name = None  # Inline
        source_mapping = {
            'naam': 'itemnaam'
        }
        fields = (
            'naam',
            'vraagstelling',
            'verplicht',
            'toelichting',
        )


class StatusTypeSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_uuid': 'is_van__uuid',
        'catalogus_uuid': 'is_van__maakt_deel_uit_van__uuid',
    }

    is_van = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'maakt_deel_uit_van__uuid',
        },
    )
    # heeftVerplichteEigenschap = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='heeft_verplichte_eigenschap',
    #     view_name='api:eigenschap-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
    #         'zaaktype_pk': 'is_van__pk'
    #     },
    # )
    # heeftVerplichteZaakObjecttype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='heeft_verplichte_zaakobjecttype',
    #     view_name='api:zaakobjecttype-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
    #         'zaaktype_pk': 'is_relevant_voor__pk',
    #     },
    # )
    # heeftVerplichteInformatieobjecttype = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     source='heeft_verplichte_zit',
    #     view_name='api:zktiot-detail',
    #     parent_lookup_kwargs={
    #         'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
    #         'zaaktype_pk': 'zaaktype__pk',
    #     },
    # )

    class Meta:
        model = StatusType
        fields = (
            'url',
            'omschrijving',
            'omschrijving_generiek',
            'statustekst',

            'is_van',

            # 'volgnummer',
            # 'doorlooptijd',
            # 'checklistitem',
            # 'informeren',
            # 'toelichting',

            # 'ingangsdatumObject',
            # 'einddatumObject',

            # 'heeftVerplichteInformatieobjecttype',
            # 'heeftVerplichteEigenschap',
            # 'heeftVerplichteZaakObjecttype',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'omschrijving': {
                'source': 'statustype_omschrijving',
            },
            'omschrijving_generiek': {
                'source': 'statustype_omschrijving_generiek',
            }
        }
