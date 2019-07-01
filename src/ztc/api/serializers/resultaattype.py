from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from vng_api_common.constants import Archiefnominatie
from vng_api_common.serializers import (
    GegevensGroepSerializer, NestedGegevensGroepMixin,
    add_choice_values_help_text
)

from ...datamodel.models import ResultaatType


class BrondatumArchiefprocedureSerializer(GegevensGroepSerializer):
    class Meta:
        model = ResultaatType
        gegevensgroep = 'brondatum_archiefprocedure'


class ResultaatTypeSerializer(NestedGegevensGroepMixin, serializers.HyperlinkedModelSerializer):

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
            },
            'zaaktype': {
                'lookup_field': 'uuid',
                'label': _('is van'),
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['archiefnominatie'].help_text += '\n\n{}'.format(add_choice_values_help_text(Archiefnominatie))
