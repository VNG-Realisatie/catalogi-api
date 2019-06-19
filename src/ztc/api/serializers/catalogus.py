from rest_framework import serializers

from ...datamodel.models import Catalogus


class CatalogusSerializer(serializers.HyperlinkedModelSerializer):
    zaaktypen = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaaktype_set',
        view_name='zaaktype-detail',
        lookup_field='uuid',
    )

    besluittypen = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='besluittype-detail',
        lookup_field='uuid',
    )

    informatieobjecttypen = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='informatieobjecttype_set',
        view_name='informatieobjecttype-detail',
        lookup_field='uuid',
    )

    class Meta:
        model = Catalogus
        fields = (
            'url',
            'domein',
            'rsin',
            'contactpersoon_beheer_naam',
            'contactpersoon_beheer_telefoonnummer',
            'contactpersoon_beheer_emailadres',
            'zaaktypen',
            'besluittypen',
            'informatieobjecttypen',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
        }
