from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from zds_schema.constants import Archiefnominatie
from zds_schema.serializers import (
    GegevensGroepSerializer, add_choice_values_help_text
)

from ...datamodel.models import ResultaatType


class BrondatumArchiefprocedureSerializer(GegevensGroepSerializer):
    class Meta:
        model = ResultaatType
        gegevensgroep = 'brondatum_archiefprocedure'


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

    brondatum_archiefprocedure = BrondatumArchiefprocedureSerializer(
        label=_("Brondatum archiefprocedure"),
        required=False,
        help_text=("Specificatie voor het bepalen van de brondatum voor de "
                   "start van de Archiefactietermijn (=brondatum) van het zaakdossier.")
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
            'archiefnominatie',
            'brondatum_archiefprocedure',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['archiefnominatie'].help_text += '\n\n{}'.format(add_choice_values_help_text(Archiefnominatie))
