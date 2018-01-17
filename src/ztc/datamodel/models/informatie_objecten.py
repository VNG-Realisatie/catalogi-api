from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...utils.stuff_date import parse_onvolledige_datum
from ..choices import VertrouwelijkheidAanduiding
from .mixins import GeldigheidMixin


class InformatieObjectTypeOmschrijvingGeneriek(GeldigheidMixin, models.Model):
    """
    Algemeen binnen de overheid gehanteerde omschrijvingen van de typen informatieobjecten

    **Toelichting referentielijst**
    Deze 'lijst' bevat de benamingen van de generieke informatieobjecttypen die in de informatie-uitwisseling betrokken
    zijn.

    Het gaat telkens om een korte omschrijving van de aard van een informatieobject, ook wel 'documentnaam' genoemd,
    zoals deze landelijk binnen de overheid wordt toegepast op basis van de ZTC. De 'lijst' betreft dus geen
    informatieobjecttypen voor specifieke domeinen en ook geen organisatiespecifieke informatieobjecttypen.

    """
    informatieobjecttype_omschrijving_generiek = models.CharField(
        _('informatieobjecttype omschrijving generiek'), max_length=80,
        help_text=_('Algemeen gehanteerde omschrijving van het type informatieobject.'))
    definitie_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('definitie'), max_length=255,
        help_text=_('Nauwkeurige beschrijving van het generieke type informatieobject'))
    herkomst_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('herkomst'), max_length=12,
        help_text=_('De naam van de waardenverzameling, of van de beherende organisatie daarvan, waaruit de waarde is overgenomen.'))
    hierarchie_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('hierarchie'), max_length=80,
        help_text=_('De plaats in de rangorde van het informatieobjecttype.'))
    opmerking_informatieobjecttype_omschrijving_generiek = models.CharField(
        _('opmerking'), max_length=255, blank=True, null=True,
        help_text=_('Zinvolle toelichting bij het informatieobjecttype'))

    class Meta:
        mnemonic = 'DOG'
        verbose_name = _('Generieke informatieobjecttype-omschrijving')
        verbose_name_plural = _('Generieke informatieobjecttype-omschrijvingen')

    def clean(self):
        """
        Er is alleen een regel voor datum_einde_geldigheid:
        Alleen een datum die gelijk is aan of die gelegen is na de datum zoals opgenomen onder 'Datum
        begin geldigheid’ kan in de registratie worden opgenomen.
        """
        if self.datum_einde_geldigheid:
            datum_begin = parse_onvolledige_datum(self.datum_begin_geldigheid)
            datum_einde = parse_onvolledige_datum(self.datum_einde_geldigheid)

            if datum_einde < datum_begin:
                raise ValidationError(_("'Datum einde geldigheid' moet gelijk zijn aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid’"))


class InformatieObjectType(GeldigheidMixin, models.Model):
    """
    Aanduiding van de aard van INFORMATIEOBJECTen zoals gehanteerd door de zaakbehandelende organisatie.

    Unieke aanduiding van CATALOGUS in combinatie met Informatieobjecttype-omschrijving.
    """
    informatieobjecttype_omschrijving = models.CharField(
        _('omschrijving'), max_length=80,
        help_text=_('Omschrijving van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE.'))
    informatieobjecttype_omschrijving_generiek = models.ForeignKey(
        'datamodel.InformatieObjectTypeOmschrijvingGeneriek', verbose_name=_('omschrijving generiek'),
        blank=True, null=True, help_text=_('Algemeen gehanteerde omschrijving van het INFORMATIEOBJECTTYPE.'))
    informatieobjectcategorie = models.CharField(
        _('categorie'), max_length=80,
        help_text=_('Typering van de aard van informatieobjecten van dit INFORMATIEOBJECTTYPE.'))
    informatieobjecttypetrefwoord = ArrayField(models.CharField(
        _('trefwoord'), max_length=30,
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

    zaaktypes = models.ManyToManyField(
        'datamodel.Zaaktype', verbose_name=_('zaaktypes'), related_name='heeft_relevant_informatieobjecttype',
        through='datamodel.ZaakInformatieobjectType', help_text=_(
            'ZAAKTYPE met ZAAKen die relevant kunnen zijn voor dit INFORMATIEOBJECTTYPE'))

    class Meta:
        mnemonic = 'DCT'
        unique_together = ('maakt_deel_uit_van', 'informatieobjecttype_omschrijving')
        verbose_name = _('Informatieobjecttype')
        verbose_name_plural = _('Informatieobjecttypen')

    def clean(self):
        """
        Voor datum_begin_geldigheid geldt:
        - De datum is gelijk aan een Versiedatum van een gerelateerd zaaktype.

        Voor datum_einde_geldigheid geldt:
        - De datum is gelijk aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid informatieobjecttype’.
        - De datum is gelijk aan de dag voor een Versiedatum van een gerelateerd zaaktype.
        """
        if self.datum_einde_geldigheid:
            datum_begin = parse_onvolledige_datum(self.datum_begin_geldigheid)
            datum_einde = parse_onvolledige_datum(self.datum_einde_geldigheid)

            if datum_einde < datum_begin:
                raise ValidationError(_(
                    "'Datum einde geldigheid' moet gelijk zijn aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid’"))

    def __str__(self):
        return '{} - {}'.format(self.maakt_deel_uit_van, self.informatieobjecttype_omschrijving)
