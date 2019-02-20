from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from ...datamodel.models import ResultaatType


class ResultaatTypeSerializer(serializers.HyperlinkedModelSerializer):

    zaaktype = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name='zaaktype-detail',
        lookup_field='uuid',
        parent_lookup_kwargs={
            'catalogus_uuid': 'catalogus__uuid',
        },
        label=_('is van')
    )

    _omschrijving_generiek = serializers.ReadOnlyField(
        help_text=_("Waarde van de omschrijving-generiek referentie (attribuut `omschrijving`)")
    )

    class Meta:
        model = ResultaatType
        fields = (
            'url',
            'zaaktype',
            'omschrijving',
            'omschrijving_generiek',
            '_omschrijving_generiek',
            'selectielijstklasse',
            # TODO: procestermijn + bewaartermijn + archiefnominatie
            'toelichting',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
        }
