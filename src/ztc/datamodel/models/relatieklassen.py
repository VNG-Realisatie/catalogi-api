from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ztc.datamodel.choices import AardRelatieChoices, ArchiefNominatieChoices, RichtingChoices


class ZaakInformatieobjectType(models.Model):
    """
    ZAAK-INFORMATIEOBJECT-TYPE

    Kenmerken van de relatie ZAAKTYPE heeft relevante INFORMATIEOBJECTTYPEn.
    """
    volgnummer = models.IntegerField(
        _('volgnummer'), validators=[MaxValueValidator(999)], help_text=_(
            'Uniek volgnummer van het ZAAK-INFORMATIEOBJECT-TYPE binnen het ZAAKTYPE.'))
    richting = models.CharField(_('richting'), max_length=20, choices=RichtingChoices.choices, help_text=_(
        'Aanduiding van de richting van informatieobjecten van het gerelateerde INFORMATIEOBJECTTYPE '
        'bij zaken van het gerelateerde ZAAKTYPE.'))

    informatie_object_type = models.ForeignKey('datamodel.InformatieObjectType')
    zaaktype = models.ForeignKey('datamodel.Zaaktype')

    status_type = models.ForeignKey(
        'datamodel.StatusType', verbose_name=_('status type'), blank=True, null=True,
        related_name='heeft_verplichte_zit', help_text=_(
            'De informatieobjecten van de INFORMATIEOBJECTTYPEn van het aan het STATUSTYPE gerelateerde ZAAKTYPE '
            'waarvoor geldt dat deze verplicht aanwezig moeten zijn bij een zaak van het gerelateerde ZAAKTYPE '
            'voordat de status van dit STATUSTYPE kan worden gezet bij die zaak.'))


class ZaakInformatieobjectTypeArchiefregime(models.Model):
    """
    ZAAK-INFORMATIETOBJECT-TYPE ARCHIEFREGIME

    Afwijkende archiveringskenmerken van informatieobjecten van een
    INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op grond van
    resultaten van een RESULTAATTYPE bij dat ZAAKTYPE
    """
    # TODO [KING]:  waardenverzameling 'de aanduidingen van de passages cq. klassen in de gehanteerde selectielijst.'
    selectielijstklasse = models.CharField(
        _('selectielijstklasse'), max_length=500, blank=True, null=True, help_text=_(
            'Verwijzing naar de voor het ZAAKINFORMATIEOBJECTTYPE bij het RESULTAATTYPE relevante passage in de '
            'Selectielijst Archiefbescheiden van de voor het ZAAKTYPE verantwoordelijke overheidsorganisatie.'))
    # choices  Blijvend bewaren Vernietigen
    archiefnominatie = models.CharField(
        _('archiefnominatie'), max_length=16, choices=ArchiefNominatieChoices.choices, help_text=_(
            'Aanduiding die aangeeft of informatieobjecten, van het INFORMATIEOBJECTTYPE bij zaken van het '
            'ZAAKTYPE met een resultaat van het RESULTAATTYPE, blijvend moeten worden bewaard of (op termijn) '
            'moeten worden vernietigd.'))
    archiefactietermijn = models.PositiveSmallIntegerField(
        _('archiefactietermijn'), validators=[MaxValueValidator(9999)], help_text=_(
            'De termijn waarna informatieobjecten, van het INFORMATIEOBJECTTYPE bij zaken van het ZAAKTYPE '
            'met een resultaat van het RESULTAATTYPE, vernietigd of overgebracht (naar een archiefbewaarplaats) '
            'moeten worden.'))

    zaak_informatieobject_type = models.ForeignKey('datamodel.ZaakInformatieobjectType')
    resultaattype = models.ForeignKey('datamodel.ResultaatType')

    class Meta:
        mnemonic = 'ZIA'


class ZaakTypenRelatie(models.Model):
    """
    ZAAKTYPENRELATIE

    Kenmerken van de relatie ZAAKTYPE heeft gerelateerde ZAAKTYPE.
    """
    aard_relatie = models.CharField(_('aard relatie'), max_length=15, choices=AardRelatieChoices.choices, help_text=_(
        'Omschrijving van de aard van de relatie van zaken van het ZAAKTYPE tot zaken van het andere ZAAKTYPE'))
    toelichting = models.CharField(_('toelichting'), max_length=255, blank=True, null=True, help_text=_(
        'Een toelichting op de aard van de relatie tussen beide ZAAKTYPEN.'))

    zaaktype = models.ForeignKey('datamodel.ZaakType', related_name='zaaktype_relatie_van')
    zaaktype = models.ForeignKey('datamodel.ZaakType', related_name='zaaktype_relatie_naar')
