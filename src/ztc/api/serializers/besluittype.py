from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
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

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)

        # check that M2M relations are created only with draft objects
        informatieobjecttypes = validated_attrs.get('informatieobjecttypes', [])
        zaaktypes = validated_attrs.get('zaaktypes', [])
        for related_objects in [informatieobjecttypes, zaaktypes]:
            for related_object in related_objects:
                if not related_object.draft:
                    msg = _("Relations to a non-draft object can't be created")
                    raise PermissionDenied(detail=msg)

        return validated_attrs
