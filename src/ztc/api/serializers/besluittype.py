from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from ...datamodel.models import BesluitType, InformatieObjectType, ZaakType


class BesluitTypeSerializer(serializers.HyperlinkedModelSerializer):
    informatieobjecttypes = serializers.HyperlinkedRelatedField(
        view_name='informatieobjecttype-detail',
        many=True,
        lookup_field='uuid',
        queryset=InformatieObjectType.objects.all()
    )

    zaaktypes = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
        queryset=ZaakType.objects.all()
    )

    class Meta:
        model = BesluitType
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'catalogus': {
                'lookup_field': 'uuid',
            },
            'begin_geldigheid': {
                'source': 'datum_begin_geldigheid'
            },
            'einde_geldigheid': {
                'source': 'datum_einde_geldigheid'
            },
            'draft': {
                'read_only': True,
            },
        }
        fields = (
            'url',
            'catalogus',
            'zaaktypes',

            'omschrijving',
            'omschrijving_generiek',
            'besluitcategorie',
            'reactietermijn',
            'publicatie_indicatie',
            'publicatietekst',
            'publicatietermijn',
            'toelichting',

            'informatieobjecttypes',
            'begin_geldigheid',
            'einde_geldigheid',
            'draft',
        )
