from rest_framework import serializers

from ...datamodel.models import BesluitType
from ..utils.rest_flex_fields import FlexFieldsSerializerMixin


class BesluitTypeSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    maakt_deel_uit_van = serializers.HyperlinkedIdentityField(view_name='api:catalogus-detail')

    class Meta:
        model = BesluitType
        fields = (
            'besluittype_omschrijving',
            'besluittype_omschrijving_generiek',
            'besluitcategorie',
            'reactietermijn',
            'publicatie_indicatie',
            'publicatietekst',
            'publicatietermijn',
            'toelichting',
            'maakt_deel_uit_van',
            # 'wordt_vastgelegd_in',
        )
