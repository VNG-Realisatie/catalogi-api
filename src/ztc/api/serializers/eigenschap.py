from rest_framework import serializers, status
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import Eigenschap
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class EigenschapSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Eigenschap

        fields = (
            'eigenschapnaam',
            'definitie',
            'toelichting',
            'status_type',
            # 'is_van',  # TODO: works after 'zaaktype-detail' exists


            # TODO: look at xsd, use nested serializers instead of the properties
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

    extra_kwargs = {
        'is_van': {
            'view_name': 'api:zaaktype-detail'
        }
    }

    #  On BesluitType, also remove the line on the serializer
    # extra_kwargs = {
    #     'maakt_deel_uit_van': {
    #         'view_name': 'api:catalogus-detail'
    #     }
    # }
