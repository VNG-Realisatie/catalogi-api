from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.datamodel.choices import JaNee
from .mixins import GeldigheidMixin


class BesluitType(GeldigheidMixin, models.Model):
    """
    Generieke aanduiding van de aard van een besluit

    Populatie: Alle besluittypen van de besluiten die het resultaat kunnen zijn van het
    zaakgericht werken van de behandelende organisatie(s).

    Toelichting objecttype:
    Het betreft de indeling of groepering van besluiten naar hun aard, zoals bouwvergunning,
    ontheffing geluidhinder en monumentensubsidie
    """
    besluittype_omschrijving = models.CharField(
        _('besluittype omschrijving'), max_length=80, blank=True, null=True,
        help_text=_('Omschrijving van de aard van BESLUITen van het BESLUITTYPE.'))
    besluittype_omschrijving_generiek = models.CharField(
        _('besluittype omschrijving generiek'), max_length=80, blank=True, null=True,
        help_text=_('Algemeen gehanteerde omschrijving van de aard van BESLUITen van het BESLUITTYPE'))
    # TODO [KING]: waardenverzameling gebaseerd op de AWB, wat betekend dat?
    besluitcategorie = models.CharField(
        _('besluitcategorie'), max_length=40, blank=True, null=True,
        help_text=_('Typering van de aard van BESLUITen van het BESLUITTYPE.'))
    reactietermijn = models.PositiveSmallIntegerField(
        _('reactietermijn'), validators=[MaxValueValidator(999)],
        help_text=_('Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, waarbinnen verweer tegen '
                    'een besluit van het besluittype mogelijk is.'))
    publicatie_indicatie = models.CharField(
        _('publicatie indicatie'), max_length=1, choices=JaNee.choices,
        help_text=_('Aanduiding of BESLUITen van dit BESLUITTYPE gepubliceerd moeten worden.'))
    publicatietekst = models.TextField(
        _('publicatietekst'), max_length=1000, blank=True, null=True,
        help_text=_('De generieke tekst van de publicatie van BESLUITen van dit BESLUITTYPE'))
    publicatietermijn = models.PositiveSmallIntegerField(
        _('publicatietermijn'), blank=True, null=True, validators=[MaxValueValidator(999)],
        help_text=_('Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, dat BESLUITen van dit '
                    'BESLUITTYPE gepubliceerd moeten blijven.'))
    toelichting = models.TextField(
        _('toelichting'), max_length=1000, blank=True, null=True,
        help_text=_('Een eventuele toelichting op dit BESLUITTYPE.'))

    maakt_deel_uit_van = models.ForeignKey(
        'datamodel.Catalogus', verbose_name=_('maakt deel uit van Catalogus'),
        help_text=_('De CATALOGUS waartoe dit BESLUITTYPE behoort.'))
    wordt_vastgelegd_in = models.ManyToManyField(
        'datamodel.InformatieObjectType', blank=True,
        help_text=_('Het INFORMATIEOBJECTTYPE van informatieobjecten waarin besluiten van dit BESLUITTYPE worden vastgelegd.'))

    class Meta:
        mnemonic = 'BST'
        unique_together = ('maakt_deel_uit_van', 'besluittype_omschrijving')

    def __str__(self):
        """
        Unieke aanduiding van CATALOGUS in combinatie met Besluittype-omschrijving
        """
        return '{} - {}'.format(self.maakt_deel_uit_van, self.besluittype_omschrijving)


