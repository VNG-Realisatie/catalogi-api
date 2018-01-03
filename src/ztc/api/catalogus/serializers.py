from drf_openapi.entities import VersionedSerializers
from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from ..besluittype.serializers import BesluitTypeSerializer
from ...datamodel.models import Catalogus


class CatalogusSerializer(SerializerExtensionsMixin, serializers.HyperlinkedModelSerializer):
    # Example mapping to a different API field.
    # naam = serializers.ModelField(Catalogus._meta.get_field('contactpersoon_beheer_naam'))

    besluittypen = HyperlinkedRelatedField(
        many=True,
        read_only=True,
        source='besluittype_set',
        view_name='besluittype-detail',
    )

    class Meta:
        model = Catalogus
        fields = (
            'domein',
            'rsin',
            'contactpersoon_beheer_naam',
            'contactpersoon_beheer_telefoonnummer',
            'contactpersoon_beheer_emailadres',
            'besluittypen',
        )
        # FIXME: This screws up field ordering...
        expandable_fields = dict(
            besluittypen=dict(
                serializer=BesluitTypeSerializer,
                many=True,
                source='besluittype_set',
            ),
        )

# http://localhost:8000/api/v1/catalogussen/?format=json&expand=besluittypen
# http://localhost:8000/api/v1/catalogussen/?format=json
#
# class CatalogusSerializer(VersionedSerializers):
#     """
#     Changelog:
#
#     * **v1.0**: Initial version
#     """
#     VERSION_MAP = (
#         ('>=1', CatalogusSerializerV1),
#     )
