from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class JaNee(DjangoChoices):
    ja = ChoiceItem('J', _('Ja'))
    nee = ChoiceItem('N', _('Nee'))


class FormaatChoices(DjangoChoices):
    tekst = ChoiceItem('tekst', _('tekst'))
    getal = ChoiceItem('getal', _('getal'))
    datum = ChoiceItem('datum', _('datum (jjjjmmdd)'))
    datum_tijd = ChoiceItem('datum_tijd', _('datum (jjjjmmdduummss)'))


class VertrouwelijkheidAanduiding(DjangoChoices):
    zeer_geheim = ChoiceItem('zeer_geheim', _('zeer geheim'))
    geheim = ChoiceItem('geheim', _('geheim'))
    confidentieel = ChoiceItem('confidentieel', _('confidentieel'))
    vertrouwelijk = ChoiceItem('vertrouwelijk', _('vertrouwelijk'))
    zaakvertrouwelijk = ChoiceItem('zaakvertrouwelijk', _('zaakvertrouwelijk'))
    intern = ChoiceItem('intern', _('intern'))
    beperkt_openbaar = ChoiceItem('beperkt_openbaar', _('beperkt openbaar'))
    openbaar = ChoiceItem('openbaar', _('openbaar'))
