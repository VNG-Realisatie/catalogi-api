from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Catalogus


class CatalogusSerializer(serializers.HyperlinkedModelSerializer):
    zaaktypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='zaaktype_set',
        view_name='zaaktype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'},
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
        )
