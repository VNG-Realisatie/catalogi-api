from django.utils.translation import ugettext_lazy as _

from relativedeltafield import format_relativedelta
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from vng_api_common.constants import Archiefnominatie
from vng_api_common.serializers import (
    GegevensGroepSerializer, add_choice_values_help_text
)

from ...datamodel.models import ResultaatType


class BrondatumArchiefprocedureSerializer(GegevensGroepSerializer):
    class Meta:
        model = ResultaatType
        gegevensgroep = 'brondatum_archiefprocedure'


    def to_representation(self, instance) -> dict:
        """
        Output the result of accessing the descriptor.
        """
        if instance.get('procestermijn'):
            instance['procestermijn'] = format_relativedelta(instance['procestermijn'])
        return instance


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
            'resultaattypeomschrijving',
            'omschrijving_generiek',
            'selectielijstklasse',
            'toelichting',
            'archiefnominatie',
            'archiefactietermijn',
            'brondatum_archiefprocedure',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            },
            'omschrijving_generiek': {
                'read_only': True,
                'help_text': _("Waarde van de omschrijving-generiek referentie (attribuut `omschrijving`)"),
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['archiefnominatie'].help_text += '\n\n{}'.format(add_choice_values_help_text(Archiefnominatie))
