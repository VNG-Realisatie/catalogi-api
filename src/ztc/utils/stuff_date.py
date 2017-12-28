from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class IndicatieOnvolledigeDatum(DjangoChoices):
    J = ChoiceItem('J', _('de datum heeft een waarde maar jaar, maand en dag zijn onbekend'), date_format='J', date_length=1)
    M = ChoiceItem('M', _('de datum heeft een waarde maar maand en dag zijn onbekend'), date_format='M%Y', date_length=5)
    D = ChoiceItem('D', _('de datum heeft een waarde maar de dag is onbekend'), date_format='D%Y%m', date_length=7)
    V = ChoiceItem('V', _('datum is volledig'), date_format='V%Y%m%d', date_length=9)


def parse_onvolledige_datum(onvolledige_datum):
    """
    Return a python datetime.date instance if the datum could be parsed

    Onvolledige datum has to be a string, first character has to be one of the
    IndicatorChoices, and the complete date string should comply to the format specified
    for that specific IndicatorChoice

    Raise one ValidationError for all error cases.
    """
    try:
        indicator_choice = IndicatieOnvolledigeDatum.get_choice(onvolledige_datum[0])
        format = indicator_choice.date_format
        assert len(onvolledige_datum) == indicator_choice.date_length
        return datetime.strptime(onvolledige_datum, format).date()
    except Exception:
        raise ValidationError(_("Onvolledige datum '{}' heeft een onbekend formaat.".format(onvolledige_datum)))
