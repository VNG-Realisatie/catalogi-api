from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.utils.stuff_date import parse_onvolledige_datum
from ..choices import RolTypeOmschrijving
from .mixins import GeldigheidMixin


class RolType(GeldigheidMixin, models.Model):
    """
    Generieke aanduiding van de aard van een ROL die een BETROKKENE kan
    uitoefenen in ZAAKen van een ZAAKTYPE.

    Toelichting objecttype
    Zowel in de GEMMA-procesarchitectuur, het RGBZ als de ZTC komt het begrip ‘rol’ voor. De
    interpretatie daarvan hebben we geharmoniseerd.
    Onder ‘rol’ verstaan we de aard van de bijdrage die een extern persoon, medewerker, afdeling,
    bedrijf e.d. levert aan de behandeling van een zaak cq. de uitvoering van een bedrijfsproces.
    Het gaat hierbij om ‘wat’ iemand doet, niet om ‘wie’ het doet. Het gaat dus niet om functies
    van medewerkers binnen een organisatie maar om de taken die iemand uitvoert. Een rol kan in
    praktijksituaties dan ook toegewezen worden aan diverse functionarissen, afdelingen en
    externen. Ook kan het voor komen dat één medewerker meerdere rollen vervult of dat
    meerdere medewerkers samen één rol vervullen.
    Rolbenamingen zijn veelal specifiek voor het zaak- of procestype: subsidieaanvrager,
    inspecteur, juridisch adviseur, vergunningbehandelaar, bezwaarindiener, klager, etcetera. Om
    bij uitwisseling van zaak- en procesgegevens (binnen en tussen organisaties) te bereiken dat
    rolbenamingen juist geïnterpreteerd worden, hanteren we generieke rolbenamingen. Per
    zaaktype en proces kunnen deze verbijzonderd of zelfs uitgesplitst worden naar context-
    specifieke benamingen. Waar gesproken wordt van ‘zaak’ bedoelen we zowel ‘hoofdzaak’ als
    ‘deelzaak’.
    """
    roltypeomschrijving = models.CharField(_('roltypeomschrijving'), max_length=20, help_text=_(
        'Omschrijving van de aard van de ROL.'))
    # TODO: er is een regel voor omschrijving generiek, deze is er ook voor vele andere modellen/velden
    roltypeomschrijving_generiek = models.CharField(
        _('roltypeomschrijving generiek'), max_length=20, choices=RolTypeOmschrijving.choices,
        help_text=_('Algemeen gehanteerde omschrijving van de aard van de ROL.'))
    # TODO: soort_betrokkene heeft kardinaliteit 1 - N, dus de ArrayField moet minsten 1 item afwdingen
    soort_betrokkene = ArrayField(models.CharField(
        _('soort betrokkene'), max_length=80, help_text=_('De (soort) betrokkene die een rol van dit roltype mag uitoefenen.')))

    is_van = models.ForeignKey('datamodel.ZaakType', verbose_name=_('is van'), help_text=_(
        'De ROLTYPEn waarin BETROKKENEn een ROL kunnen uitoefenen in ZAAKen van dit ZAAKTYPE.'))

    class Meta:
        mnemonic = 'RLT'
        unique_together = ('is_van', 'roltypeomschrijving')

    def clean(self):
        """
        datum_begin_geldigheid is gelijk aan een Versiedatum van het gerelateerde zaaktype.

        datum_einde_geldigheid
        De datum is gelijk aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid roltype’.
        De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype.
        """
        datum_begin = parse_onvolledige_datum(self.datum_begin_geldigheid)
        versiedatum = parse_onvolledige_datum(self.is_van.versiedatum)

        if datum_begin != versiedatum:
            raise ValidationError(
                _("De datum_begin_geldigheid moet gelijk zijn aan een Versiedatum van het gerelateerde zaaktype."))

        if self.datum_einde_geldigheid:
            datum_einde = parse_onvolledige_datum(self.datum_einde_geldigheid)

            if datum_einde < datum_begin:
                raise ValidationError(_(
                    "'Datum einde geldigheid' moet gelijk zijn aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid’"))

            if datum_einde + timedelta(days=1) != versiedatum:
                raise ValidationError(_(
                    "'Datum einde geldigheid' moet gelijk zijn aan de dag voor een Versiedatum van het gerelateerde zaaktype."))

    def __str__(self):
        return '{} - {}'.format(self.is_van, self.roltypeomschrijving)
