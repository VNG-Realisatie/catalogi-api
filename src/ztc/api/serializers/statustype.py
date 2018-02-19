from rest_framework.serializers import ModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import CheckListItem, StatusType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
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


class StatusTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_pk': 'is_van__pk',
        'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
    }

    isVan = NestedHyperlinkedRelatedField(
        read_only=True,
        source='is_van',
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'maakt_deel_uit_van__pk',
        },
    )
    heeftVerplichteEigenschap = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_verplichte_eigenschap',
        view_name='api:eigenschap-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'is_van__pk'
        },
    )
    heeftVerplichteZaakObjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_verplichte_zaakobjecttype',
        view_name='api:zaakobjecttype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_relevant_voor__maakt_deel_uit_van__pk',
        },
    )
    heeftVerplichteInformatieobjecttype = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='heeft_verplichte_zit',
        view_name='api:zktiot-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'zaaktype__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'zaaktype__pk',
        },
    )

    class Meta:
        model = StatusType
        ref_name = model.__name__
        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',
            'doorlooptijd': 'doorlooptijd_status',
            'volgnummer': 'statustypevolgnummer',
            'omschrijvingGeneriek': 'statustype_omschrijving_generiek',
            'omschrijving': 'statustype_omschrijving',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:statustype-detail'},
        }
        fields = (
            'url',
            'omschrijving',
            'omschrijvingGeneriek',
            'volgnummer',
            'doorlooptijd',
            'checklistitem',
            'informeren',
            'statustekst',
            'toelichting',

            'ingangsdatumObject',
            'einddatumObject',

            'isVan',
            'heeftVerplichteInformatieobjecttype',
            'heeftVerplichteEigenschap',
            'heeftVerplichteZaakObjecttype',
        )
