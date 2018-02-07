from rest_framework import serializers

from .zaken import ZaakTypeSerializer
from ...datamodel.models import Eigenschap
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class EigenschapSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    is_van = ZaakTypeSerializer(read_only=True)

    class Meta:
        model = Eigenschap

        fields = (
            'eigenschapnaam',
            'definitie',
            'toelichting',
            'status_type',
            # 'is_van',  # TODO: currently returns all the fields from ZaakType, probably add it as a link


            # TODO: look at xsd, use nested serializers instead of the properties
            # 'attribuutsets' are a foreignkey, but made available as properties
            # 'groep',
            # 'formaat',
            # 'lengte',
            # 'kardinaliteit',
            # 'waardenverzameling',
            # 'objecttype',
            # 'informatiemodel',
            # 'namespace',
            # 'schemalocatie',
            # 'x_path_element',
            # 'entiteittype',
        )

    extra_kwargs = {
        'is_van': {
            'view_name': 'api:zaaktype-detail'
        }
    }
