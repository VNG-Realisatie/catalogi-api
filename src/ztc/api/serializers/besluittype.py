from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from ...datamodel.models import BesluitType


class BesluitTypeSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'catalogus_uuid': 'catalogus__uuid'
    }

    informatieobjecttypes = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='informatieobjecttype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        },
    )

    zaaktypes = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        }
    )

    class Meta:
        model = BesluitType
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
            'zaaktypes',

            'omschrijving',
            'omschrijving_generiek',
            'besluitcategorie',
            'reactietermijn',
            'publicatie_indicatie',
            'publicatietekst',
            'publicatietermijn',
            'toelichting',

            'informatieobjecttypes',
        )
