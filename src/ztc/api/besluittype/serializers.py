from rest_framework import serializers

from ...datamodel.models import BesluitType


class BesluitTypeSerializer(serializers.HyperlinkedModelSerializer):
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
            # 'maakt_deel_uit_van',
            # 'wordt_vastgelegd_in',
        )
