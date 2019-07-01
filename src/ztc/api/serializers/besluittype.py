from rest_framework import serializers

from ...datamodel.models import BesluitType


class BesluitTypeSerializer(serializers.HyperlinkedModelSerializer):
    informatieobjecttypes = serializers.HyperlinkedRelatedField(
        view_name='informatieobjecttype-detail',
        many=True,
        lookup_field='uuid',
        read_only=True
    )

    zaaktypes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
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
