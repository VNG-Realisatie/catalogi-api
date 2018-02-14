from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import RolType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin
from ..utils.serializers import SourceMappingSerializerMixin


class RolTypeSerializer(FlexFieldsSerializerMixin, SourceMappingSerializerMixin, NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'zaaktype_pk': 'is_van__pk',
        'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
    }
    isVan = NestedHyperlinkedIdentityField(
        view_name='api:zaaktype-detail',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
            'pk': 'is_van__pk'
        },
    )
    magZetten = NestedHyperlinkedIdentityField(
        many=True,
        view_name='api:statustype-detail',
        source='mag_zetten',
        parent_lookup_kwargs={
            'catalogus_pk': 'is_van__maakt_deel_uit_van__pk',
            'zaaktype_pk': 'is_van__pk',
        },
    )

    class Meta:
        model = RolType

        source_mapping = {
            'ingangsdatumObject': 'datum_begin_geldigheid',
            'einddatumObject': 'datum_einde_geldigheid',
            'omschrijving': 'roltypeomschrijving',
            'omschrijvingGeneriek': 'roltypeomschrijving_generiek',
            'soortBetrokkene': 'soort_betrokkene',
        }
        extra_kwargs = {
            'url': {'view_name': 'api:roltype-detail'},
        }
        fields = (
            'url',
            'ingangsdatumObject',
            'einddatumObject',
            'omschrijving',
            'omschrijvingGeneriek',
            'soortBetrokkene',
            'isVan',
            'magZetten',
        )
