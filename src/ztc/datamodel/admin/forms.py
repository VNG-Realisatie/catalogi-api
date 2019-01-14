from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import ZaakType


class BooleanRadio(forms.RadioSelect):

    def __init__(self, attrs=None):
        choices = (
            (True, _('Yes')),
            (False, _('No')),
        )
        super().__init__(attrs, choices)

    def value_from_datadict(self, data, files, name):
        value = data[name]
        return {
            True: True,
            'True': True,
            'False': False,
            False: False,
        }[value]


class ZaakTypeForm(forms.ModelForm):
    class Meta:
        model = ZaakType
        fields = '__all__'
        widgets = {
            'opschorting_en_aanhouding_mogelijk': BooleanRadio,
            'verlenging_mogelijk': BooleanRadio,
            'publicatie_indicatie': BooleanRadio,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['opschorting_en_aanhouding_mogelijk'].required = True
        self.fields['verlenging_mogelijk'].required = True
        self.fields['publicatie_indicatie'].required = True

        self.fields['trefwoorden'].help_text += ' Gebruik een komma om waarden van elkaar te onderscheiden.'
