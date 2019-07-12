from drf_writable_nested import NestedCreateMixin
from rest_framework import serializers
from vng_api_common.serializers import add_choice_values_help_text
from vng_api_common.constants import RolOmschrijving

from ...datamodel.models import MogelijkeBetrokkene, RolType


class MogelijkeBetrokkeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MogelijkeBetrokkene
        fields = (
            'betrokkene',
            'betrokkene_type',
        )


class RolTypeSerializer(NestedCreateMixin, serializers.HyperlinkedModelSerializer):
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
            'zaaktype': {
                'lookup_field': 'uuid'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(RolOmschrijving)
        self.fields['omschrijving_generiek'].help_text += f"\n\n{value_display_mapping}"
