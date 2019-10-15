import uuid as _uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from vng_api_common.fields import DaysDurationField

from .mixins import ConceptMixin, GeldigheidMixin


class BesluitType(GeldigheidMixin, ConceptMixin, models.Model):
    """
    Generieke aanduiding van de aard van een besluit.

    **Populatie**
    Alle besluittypen van de besluiten die het resultaat kunnen zijn van het
    zaakgericht werken van de behandelende organisatie(s).

    **Toelichting objecttype**
    Het betreft de indeling of groepering van besluiten naar hun aard, zoals
    bouwvergunning, ontheffing geluidhinder en monumentensubsidie.
    """

    uuid = models.UUIDField(
        unique=True, default=_uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )

    omschrijving = models.CharField(
        _("omschrijving"),
        max_length=80,
        blank=True,
        help_text=_("Omschrijving van de aard van BESLUITen van het BESLUITTYPE."),
    )

    # TODO [KING]: wat is de waardenverzameling?
    omschrijving_generiek = models.CharField(
        _("omschrijving generiek"),
        max_length=80,
        blank=True,
        help_text=_(
            "Algemeen gehanteerde omschrijving van de aard van BESLUITen van het BESLUITTYPE"
        ),
    )

    # TODO [KING]: waardenverzameling gebaseerd op de AWB, wat betekend dat?
    besluitcategorie = models.CharField(
        _("besluitcategorie"),
        max_length=40,
        blank=True,
        help_text=_("Typering van de aard van BESLUITen van het BESLUITTYPE."),
    )

    reactietermijn = DaysDurationField(
        _("reactietermijn"),
        blank=True,
        null=True,
        help_text=_(
            "Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, waarbinnen verweer tegen "
            "een besluit van het besluittype mogelijk is."
        ),
    )

    publicatie_indicatie = models.BooleanField(
        _("publicatie indicatie"),
        null=False,
        help_text=_(
            "Aanduiding of BESLUITen van dit BESLUITTYPE gepubliceerd moeten worden."
        ),
    )

    publicatietekst = models.TextField(
        _("publicatietekst"),
        blank=True,
        help_text=_(
            "De generieke tekst van de publicatie van BESLUITen van dit BESLUITTYPE"
        ),
    )

    publicatietermijn = DaysDurationField(
        _("publicatietermijn"),
        blank=True,
        null=True,
        help_text=_(
            "Het aantal dagen, gerekend vanaf de verzend- of publicatiedatum, dat BESLUITen van dit "
            "BESLUITTYPE gepubliceerd moeten blijven."
        ),
    )

    toelichting = models.TextField(
        _("toelichting"),
        blank=True,
        help_text=_("Een eventuele toelichting op dit BESLUITTYPE."),
    )

    catalogus = models.ForeignKey(
        "datamodel.Catalogus",
        on_delete=models.CASCADE,
        verbose_name=_("catalogus"),
        help_text=_(
            "URL-referentie naar de CATALOGUS waartoe dit BESLUITTYPE behoort."
        ),
    )

    informatieobjecttypes = models.ManyToManyField(
        "datamodel.InformatieObjectType",
        blank=True,
        verbose_name=_("informatieobjecttype"),
        related_name="besluittypen",
        help_text=_(
            "URL-referenties naar het INFORMATIEOBJECTTYPE van informatieobjecten waarin besluiten van dit "
            "BESLUITTYPE worden vastgelegd."
        ),
    )

    resultaattypes = models.ManyToManyField(
        "datamodel.ResultaatType",
        verbose_name=_("is resultaat van"),
        help_text=_(
            "(inverse van:) Het BESLUITTYPE van besluiten die gepaard gaan "
            "met resultaten van het RESULTAATTYPE."
        ),
    )

    zaaktypes = models.ManyToManyField(
        "datamodel.ZaakType",
        verbose_name=_("zaaktypes"),
        related_name="besluittypen",
        help_text=_(
            "ZAAKTYPE met ZAAKen die relevant kunnen zijn voor dit BESLUITTYPE"
        ),
    )

    class Meta:
        verbose_name = _("besluittype")
        verbose_name_plural = _("besluittypen")
        unique_together = ("catalogus", "omschrijving")

    def __str__(self):
        """
        Unieke aanduiding van CATALOGUS in combinatie met Besluittype-omschrijving
        """
        return f"{self.catalogus} - {self.omschrijving}"

    # def clean(self):
    #     """
    #     datum_begin_geldigheid is gelijk aan een Versiedatum van een gerelateerd zaaktype.

    #     datum_einde_geldigheid is gelijk aan de dag voor een Versiedatum van een gerelateerd zaaktype.
    #     """
    #     super().clean()
    #     TODO: review this, see GeldigheidsMixin.clean
    #     TODO: many to many can not be validated in model.clean, we need to use a form (self.zaaktypes)
    #     if self.datum_begin_geldigheid:
    #         # it is required, if it was not filled in, validation error from the field will be raised
    #         zaaktype_versiedatums = list(set(self.zaaktypes.values_list('versiedatum', flat=True)))
    #         # use the 'onvolledige datums', do not convert to python datetime.date for this comparision
    #         if self.datum_begin_geldigheid not in zaaktype_versiedatums:
    #             raise ValidationError(_('Datum_begin_geldigheid is niet gelijk aan een Versiedatum '
    #                                     'van een gerelateerd zaaktype.'))

    #     if self.datum_einde_geldigheid:
    #         zaaktype_versiedatums = list(set(self.zaaktypes.values_list('versiedatum', flat=True)))

    #         day_before_zaaktype_versie_datums = [
    #             parse_onvolledige_datum(_date) - timedelta(days=1) for _date in zaaktype_versiedatums
    #         ]
    #         if self.datum_begin_geldigheid not in day_before_zaaktype_versie_datums:
    #             raise ValidationError(
    #                 _('Datum_einde_geldigheid is niet gelijk aan de dag voor een Versiedatum '
    #                   'van een gerelateerd zaaktype.'))
