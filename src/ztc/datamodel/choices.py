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


class ArchiefNominaties(DjangoChoices):
    blijvend_bewaren = ChoiceItem('blijvend_bewaren', _('blijvend bewaren'))
    vernietigen = ChoiceItem('vernietigen', _('vernietigen'))


class ArchiefProcedure(DjangoChoices):
    afgehandeld = ChoiceItem('afgehandeld', _('afgehandeld'))
    ingangsdatum_besluit = ChoiceItem('ingangsdatum_besluit', _('ingangsdatum besluit'))
    vervaldatum_besluit = ChoiceItem('vervaldatum_besluit', _('vervaldatum besluit'))
    eigenschap = ChoiceItem('eigenschap', _('eigenschap'))
    ander_datumkenmerk = ChoiceItem('ander_datumkenmerk', _('ander datumkenmerk'))


class RolTypeOmschrijving(DjangoChoices):
    adviseur = ChoiceItem('adviseur', _('adviseur'))  # Kennis in dienst stellen van de behandeling van (een deel van) een zaak.
    behandelaar = ChoiceItem('behandelaar', _('behandelaar'))  # De vakinhoudelijke behandeling doen van (een deel van) een zaak.
    belanghebbende = ChoiceItem('belanghebbende', _('belanghebbende'))  # Vanuit eigen en objectief belang rechtstreeks betrokken zijn bij de behandeling en/of de uitkomst van een zaak.
    beslisser = ChoiceItem('beslisser', _('beslisser'))  # Nemen van besluiten die voor de uitkomst van een zaak noodzakelijk zijn.
    initiator = ChoiceItem('initiator', _('initiator'))  # Aanleiding geven tot de start van een zaak ..
    klantcontacter = ChoiceItem('klantcontacter', _('klantcontacter'))  # Het eerste aanspreekpunt zijn voor vragen van burgers en bedrijven ..
    zaakcoordinator = ChoiceItem('zaakcoordinator', _('zaakcoördinator'))  # Er voor zorg dragen dat de behandeling van de zaak in samenhang uitgevoerd wordt conform de daarover gemaakte afspraken.
