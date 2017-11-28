from djchoices import ChoiceItem, DjangoChoices
from django.utils.translation import ugettext_lazy as _


class JaNee(DjangoChoices):
    ja = ChoiceItem('J', _('Ja'))
    nee = ChoiceItem('N', _('Nee'))


class FormaatChoices(DjangoChoices):
    tekst = ChoiceItem('tekst', _('tekst'))
    getal = ChoiceItem('getal', _('getal'))
    datum = ChoiceItem('datum', _('datum (jjjjmmdd)'))
    datum_tijd = ChoiceItem('datum_tijd', _('datum (jjjjmmdduummss)'))
