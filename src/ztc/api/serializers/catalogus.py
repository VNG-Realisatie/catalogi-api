from rest_framework import serializers, status
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Catalogus
from ..serializers import BesluitTypeSerializer
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class CatalogusSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    # Example mapping to a different API field.
    # naam = serializers.ModelField(Catalogus._meta.get_field('contactpersoon_beheer_naam'))

    # Instead of the ID, the URL is used.
    url = HyperlinkedIdentityField(view_name='api:catalogus-detail')

    # Nested serializers are shown as URLs, but should be expandable (see below).
    besluittypen = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='api:besluittype-detail',
        parent_lookup_kwargs={'catalogus_pk': 'maakt_deel_uit_van__pk'}
    )

    class Meta:
        model = Catalogus
        # All fields should be included. Meta data that is not part of the ZTC information model can be left out.
        fields = (
            'url',
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
