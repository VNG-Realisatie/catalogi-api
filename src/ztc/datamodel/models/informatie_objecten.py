from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.datamodel.choices import VertrouwelijkheidAanduiding
from .mixins import GeldigheidMixin


class InformatieObjectTypeOmschrijvingGeneriek(GeldigheidMixin, models.Model):
    """
    Algemeen binnen de overheid gehanteerde omschrijvingen van de typen
    informatieobjecten

    Toelichting referentielijst
    Deze 'lijst' bevat de benamingen van de generieke informatieobjecttypen die in de informatie-
    uitwisseling betrokken zijn.
    Het gaat telkens om een korte omschrijving van de aard van een informatieobject, ook wel
    'documentnaam' genoemd, zoals deze landelijk binnen de overheid wordt toegepast op basis van de ZTC.
    De 'lijst' betreft dus geen informatieobjecttypen voor specifieke domeinen en ook geen
    organisatiespecifieke informatieobjecttypen.

    """
    informatieobjecttype_omschrijving_generiek = models.CharField(
        _('informatieobjecttype omschrijving generiek'), max_length=80,
        help_text=_('Algemeen gehanteerde omschrijving van het type informatieobject.'))
    definitie_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('definitie informatieobjecttype omschrijving generiek'), max_length=255,
        help_text=_('Nauwkeurige beschrijving van het generieke type informatieobject'))
    herkomst_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('herkomst informatieobjecttype omschrijving generiek'), max_length=12,
        help_text=_('De naam van de waardenverzameling, of van de beherende organisatie daarvan, waaruit de waarde is overgenomen.'))
    hierarchie_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('hierarchie informatieobjecttype omschrijving generiek'), max_length=80,
        help_text=_('De plaats in de rangorde van het informatieobjecttype.'))
    opmerking_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('opmerking informatieobjecttype omschrijving generiek'), max_length=255, blank=True, null=True,
        help_text=_('Zinvolle toelichting bij het informatieobjecttype'))

    class Meta:
        mnemonic = 'DOG'


# TODO: voor beide ArrayFields (trefwoord en model) check of de ArrayField leeg mag zijn. En mogelijk verander naar een m2m met een apart model
class InformatieObjectType(GeldigheidMixin, models.Model):
    """
    Aanduiding van de aard van INFORMATIEOBJECTen zoals gehanteerd door
    de zaakbehandelende organisatie.

    Unieke aanduiding van CATALOGUS in combinatie met Informatieobjecttype-
    omschrijving.
    """
    informatieobjecttype_omschrijving = models.CharField(
        _('informatieobjecttype omschrijving'), max_length=80,
        help_text=_('Omschrijving van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE.'))
    informatieobjecttype_omschrijving_generiek = models.ForeignKey(
        'datamodel.InformatieObjectTypeOmschrijvingGeneriek', verbose_name=_('informatieobjecttype omschrijving generiek'),
        blank=True, null=True, help_text=_('Algemeen gehanteerde omschrijving van het INFORMATIEOBJECTTYPE.'))
    informatieobjectcategorie = models.CharField(
        _('informatieobjectcategorie'), max_length=80,
        help_text=_('Typering van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE.'))
    informatieobjecttypetrefwoord = ArrayField(models.CharField(
        _('informatieobjecttypetrefwoord'), max_length=30,
        help_text=_('Trefwoord(en) waarmee informatieobjecten van het INFORMATIEOBJECTTYPE kunnen worden gekarakteriseerd.')))
    vertrouwelijkheidaanduiding = models.CharField(
        _('vertrouwelijkheidaanduiding'), max_length=20, blank=True, null=True, choices=VertrouwelijkheidAanduiding.choices,
        help_text=_('Aanduiding van de mate waarin informatieobjecten van dit INFORMATIEOBJECTTYPE voor de openbaarheid bestemd zijn.'))
    model = ArrayField(models.URLField(_('model'), help_text=_(
        'De URL naar het model / sjabloon dat wordt gebruikt voor de creatie van informatieobjecten van dit INFORMATIEOBJECTTYPE.')))
    toelichting = models.TextField(
        _('toelichting'), max_length=1000, blank=True, null=True,
        help_text=_('Een eventuele toelichting op dit INFORMATIEOBJECTTYPE.'))

    maakt_deel_uit_van = models.ForeignKey('datamodel.Catalogus', verbose_name=_('maakt deel uit van'),
                                           help_text=('De CATALOGUS waartoe dit INFORMATIEOBJECTTYPE behoort.'))

    class Meta:
        mnemonic = 'DCT'
        unique_together = ('maakt_deel_uit_van', 'informatieobjecttype_omschrijving')
