from rest_framework import serializers, status
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Eigenschap
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class EigenschapSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:eigenschap-detail')

    class Meta:
        model = Eigenschap

        fields = (
            'url',
            'eigenschapnaam',
            'definitie',
            'toelichting',
            'status_type',
            'is_van',

            # 'attribuutsets' are a foreignkey, but made available as properties
            'groep',
            'formaat',
            'lengte',
            'kardinaliteit',
            'waardenverzameling',
            'objecttype',
            'informatiemodel',
            'namespace',
            'schemalocatie',
            'x_path_element',
            'entiteittype',
        )
