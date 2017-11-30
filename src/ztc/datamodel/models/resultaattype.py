from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.utils.stuff_date import parse_onvolledige_datum
from ..choices import ArchiefNominaties, ArchiefProcedure
from .mixins import GeldigheidMixin


class ResultaatType(GeldigheidMixin, models.Model):
    """
    Het betreft de indeling of groepering van resultaten van zaken van hetzelfde
    ZAAKTYPE naar hun aard, zoals 'verleend', 'geweigerd', 'verwerkt', et cetera.

    Toelichting objecttype
    Elke zaak heeft een resultaat. In een aantal gevallen valt dit resultaat samen met een besluit:
    ‘Evenementenvergunning verleend’, ‘Energiesubsidie geweigerd’, et cetera. Het komt echter
    ook voor dat zaken worden afgehandeld zonder dat er een besluit wordt genomen. Dit is
    bijvoorbeeld het geval bij aangiften (geboorte, verhuizing), meldingen (openbare ruimte), maar
    ook bij het intrekken van een aanvraag. Het resultaat van een zaak is van groot belang voor de
    archivering: het resultaattype bepaalt mede of de zaak en het bijbehorende dossier moeten
    worden vernietigd (na enige termijn) of blijvend bewaard moeten worden (en na enige termijn
    ‘overgebracht’ worden naar een archiefbewaarplaats). Met RESULTAATTYPE worden de
    mogelijke resultaten benoemd bij het desbetreffende zaaktype. Daarmee is het archiefregime
    bepaald voor het gehele zaakdossier: alle informatie over en documenten bij de zaken van het
    ZAAKTYPE.
    In uitzonderingsgevallen kan er sprake van zijn dat documenten van een bepaald
    INFORMATIEOBJECTTYPE in zaakdossiers bij zaken van het ZAAKTYPE een afwijkend
    archiefregime hebben ten opzichte van het zaakdossier. Privacy-gevoeligheid kan er reden
    voor zijn om documenten van een ZAAKINFORMATIEOBJECTTYPE eerder te vernietigen dan het
    zaakdossier als geheel. Specifieke wetgeving, zoals die voor de BAG, leidt er daarentegen toe
    dat een Omgevingsvergunning (activiteit bouwen) ten eeuwige dage bewaard moet blijven
    terwijl het zaakdossier na 20 jaar vernietigd dient te worden. De relatiesoort ‘RESULTAATTYPE
    bepaalt afwijkend archiefregime van ZAAK-INFORMATIEOBJECT-TYPE’ geeft de mogelijkheid
    deze uitzonderingsgevallen te documenteren.
    """
    resultaattypeomschrijving = models.CharField(
        _('resultaattypeomschrijving'), max_length=20,
        help_text=_('Omschrijving van de aard van resultaten van het RESULTAATTYPE.'))
    resultaattypeomschrijving_generiek = models.CharField(
        _('resultaattypeomschrijving generiek'), max_length=20,
        help_text=_('Algemeen gehanteerde omschrijving van de aard van resultaten van het RESULTAATTYPE.'))
    # TODO: waardeverzameling is de aanduidingen van de passages cq. klassen in de gehanteerde selectielijst.
    selectielijstklasse = models.CharField(
        _('selectielijstklasse'), max_length=500, blank=True, null=True,
        help_text=_('Verwijzing naar de, voor het archiefregime bij het RESULTAATTYPE relevante, passage in de Selectielijst Archiefbescheiden van de voor het ZAAKTYPE verantwoordelijke overheidsorganisatie.'))
    archiefnominatie = models.CharField(
        _('archiefnominatie'), max_length=16, choices=ArchiefNominaties.choices,
        help_text=_('Aanduiding die aangeeft of ZAAKen met een resultaat van dit RESULTAATTYPE blijvend moeten worden bewaard of (op termijn) moeten worden vernietigd .'))
    archiefactietermijn = models.PositiveSmallIntegerField(
        _('archiefactietermijn'), validators=[MaxValueValidator(9999)],  # 0-9999 maanden
        help_text=_('De termijn waarna het zaakdossier (de ZAAK met alle bijbehorende INFORMATIEOBJECTen) van een ZAAK met een resultaat van dit RESULTAATTYPE vernietigd of overgebracht (naar een archiefbewaarplaats) moet worden.'))
    brondatum_archiefprocedure = models.CharField(
        _('brondatum archiefprocedure'), max_length=20, choices=ArchiefProcedure.choices,
        help_text=_('Aanduiding van de brondatum voor de start van de Archiefactietermijn van het zaakdossier.'))
    toelichting = models.CharField(
        _('toelichting'), max_length=1000, blank=True, null=True,
        help_text=_('Een toelichting op dit RESULTAATTYPE en het belang hiervan voor ZAAKen waarin een Resultaat van dit RESULTAATTYPE wordt geselecteerd.'))

    # TODO: relaties als de Zaak modellen er zijn
    # bepaalt_afwijkend_archiefregime_van = models.ManyToManyField(
    #     'datamodel.ZaakInformatieObjectType', verbose_name=_('bepaalt afwijkend archiefregime van'),
    #     blank=True, help_text=_(
    #         'Informatieobjecten van een ZAAKINFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE waarvan, op grond van '
    #         'resultaten van een RESULTAATTYPE bij dat ZAAKTYPE, de archiveringskenmerken afwijken van de '
    #         'archiveringskenmerken van het ZAAKTYPE.'))
    # heeft_verplichte_zot = models.ManyToManyField(
    #     'datamodel.ZaakObjectType', verbose_name=_('heeft verplichte'), blank=True, help_text=_(
    #         'De ZAAKOBJECTTYPEn die verplicht gerelateerd moeten zijn aan ZAAKen van dit ZAAKTYPE voordat een '
    #         'resultaat van dit RESULTAATTYPE kan worden gezet.'),
    # )
    # heeft_verplichte_ziot = models.ManyToManyField(  # does not have a mnemonic, I choose 'ziot' here
    #     'datamodel.ZaakInformatieObjectType', verbose_name=_(''), blank=True, help_text=_(
    #         'De INFORMATIEOBJECTTYPEn die verplicht aanwezig moeten zijn in het zaakdossier van ZAAKen van dit '
    #         'ZAAKTYPE voordat een resultaat van dit RESULTAATTYPE kan worden gezet.')
    # )
    heeft_voor_brondatum_archiefprocedure_relevante = models.ForeignKey(
        'datamodel.Eigenschap', verbose_name=_('heeft voor brondatum archiefprocedure relevante'), blank=True, null=True,
        help_text=_('De EIGENSCHAP die bepalend is voor het moment waarop de Archiefactietermijn start voor een ZAAK '
                    'met een resultaat van dit RESULTAATTYPE.'))
    # is_relevant_voor = models.ForeignKey('datamodel.ZaakType', verbose_name=_('is relevant voor'), help_text=_(
    #     'Het ZAAKTYPE van ZAAKen waarin resultaten van dit RESULTAATTYPE bereikt kunnen worden.'))

    class Meta:
        mnemonic = 'RST'
        # TODO: unique_together = ('is_relevant_voor', 'resultaattypeomschrijving')

    def clean(self):
        """
        De begin_datum is gelijk aan een Versiedatum van het gerelateerde zaaktype.

        De datum_einde_geldigheid is gelijk aan of gelegen na de datum zoals opgenomen
        onder 'Datum begin geldigheid resultaattype’.
        De datum is gelijk aan de dag voor een Versiedatum van het gerelateerde zaaktype.
        """
        datum_begin = parse_onvolledige_datum(self.datum_begin_geldigheid)
        versiedatum = parse_onvolledige_datum(self.is_relevant_voor.versiedatum)

        if datum_begin != versiedatum:
            raise ValidationError(_("De datum_begin_geldigheid moet gelijk zijn aan een Versiedatum van het gerelateerde zaaktype."))

        if self.datum_einde_geldigheid:
            datum_einde = parse_onvolledige_datum(self.datum_einde_geldigheid)

            if datum_einde < datum_begin:
                raise ValidationError(_("'Datum einde geldigheid' moet gelijk zijn aan of gelegen na de datum zoals opgenomen onder 'Datum begin geldigheid’"))

            if datum_einde + timedelta(days=1) != versiedatum:
                raise ValidationError(_("'Datum einde geldigheid' moet gelijk zijn aan de dag voor een Versiedatum van het gerelateerde zaaktype."))
