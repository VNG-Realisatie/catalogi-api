from django.core.validators import validate_integer
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..validators import validate_uppercase


class Catalogus(models.Model):
    """
    De verzameling van ZAAKTYPEn - incl. daarvoor relevante objecttypen - voor een Domein die als één geheel beheerd
    wordt.

    **Toelichting objecttype**

    Voor de inzet van de CATALOGUS in één uitvoerende organisatie (bijv. een gemeente) gaat KING ervan uit dat binnen
    de organisatie één CATALOGUS wordt gebruikt met alle ZAAKTYPEn van de organisatie. De unieke identificatie in dit
    voorbeeld wordt dan de combinatie van het Domein 'Gemeente', gevolgd door het RSIN van de betreffende gemeente.
    Standaardiserende organisaties zullen mogelijk meerdere catalogi willen publiceren en beheren. Denk aan een
    ministerie dat voor meerdere sectoren een CATALOGUS aanlegt. Via het Domein-attribuut krijgt zo elke CATALOGUS
    toch een unieke identificatie.

    KING bepaalt niet op voorhand welke waarden 'Domein' kan aannemen, maar registreert wel alle gebruikte waarden.
    """
    # TODO [KING]: "Voor de waardenverzameling wordt door KING een waardenlijst beheerd waarin wordt bijgehouden welke afkorting welk domein betreft." ZTC 2.1, blz 42 - Waar dan?
    domein = models.CharField(  # waardenverzameling hoofdletters
        _('domein'), max_length=5, validators=[validate_uppercase], help_text=_(
            'Een afkorting waarmee wordt aangegeven voor welk domein in een CATALOGUS ZAAKTYPEn zijn uitgewerkt.'))
    # TODO [KING]: rsin is gespecificeerd als N9, ivm voorloopnullen gekozen voor CharField. Geen waardenverzameling gedefinieerd
    rsin = models.CharField(
        _('rsin'), max_length=9, validators=[validate_integer],
        help_text=_('Het door een kamer toegekend uniek nummer voor de INGESCHREVEN '
                                             'NIET-NATUURLIJK PERSOON die de eigenaar is van een CATALOGUS.'))
    contactpersoon_beheer_naam = models.CharField(
        _('naam'), max_length=40,
        help_text=_('De naam van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS.'))
    contactpersoon_beheer_telefoonnummer = models.CharField(
        _('telefoonnummer'), max_length=20, blank=True, null=True,
        help_text=_('Het telefoonnummer van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS.'))
    contactpersoon_beheer_emailadres = models.EmailField(  # specificatie waardenverzameling conform RFC 5321 en RFC 5322
        _('emailadres'), max_length=254, blank=True, null=True,
        help_text=_('Het emailadres van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS.'))

    class Meta:
        mnemonic = 'CAT'
        unique_together = ('domein', 'rsin')
        verbose_name = _('Catalogus')
        verbose_name_plural = _('Catalogussen')
        ordering = unique_together

        filter_fields = ('domein', 'rsin', )
        ordering_fields = filter_fields
        search_fields = filter_fields + ('contactpersoon_beheer_naam', )

    def __str__(self):
        return '{} - {}'.format(self.domein, self.rsin)
