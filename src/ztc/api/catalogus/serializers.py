from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Catalogus
from ..besluittype.serializers import BesluitTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class CatalogusSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    # Example mapping to a different API field.
    # naam = serializers.ModelField(Catalogus._meta.get_field('contactpersoon_beheer_naam'))

    besluittypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    )

    class Meta:
        model = Catalogus
        fields = (
            'id',
            'domein',
            'rsin',
            'contactpersoon_beheer_naam',
            'contactpersoon_beheer_telefoonnummer',
            'contactpersoon_beheer_emailadres',
            'besluittypen',
        )

    expandable_fields = {
        'besluittypen': (BesluitTypeSerializer, {'source': 'besluittype_set', 'many': True})
    }
