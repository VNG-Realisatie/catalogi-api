import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from vng_api_common.caching import ETagMixin

from ztc.datamodel.choices import (
    AardRelatieChoices,
    ArchiefNominatieChoices,
    RichtingChoices,
)


class ZaakInformatieobjectType(ETagMixin, models.Model):
    """
    ZAAK-INFORMATIEOBJECT-TYPE

    Kenmerken van de relatie ZAAKTYPE heeft relevante INFORMATIEOBJECTTYPEn.
    """

    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )

    zaaktype = models.ForeignKey(
        "datamodel.Zaaktype",
        verbose_name=_("zaaktype"),
        on_delete=models.CASCADE,
        help_text=_("URL-referentie naar het ZAAKTYPE."),
    )
    informatieobjecttype = models.ForeignKey(
        "datamodel.InformatieObjectType",
        on_delete=models.CASCADE,
        verbose_name=_("informatie object type"),
        help_text=_("URL-referentie naar het INFORMATIEOBJECTTYPE."),
    )

    volgnummer = models.PositiveSmallIntegerField(
        _("volgnummer"),
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        help_text=_(
            "Uniek volgnummer van het ZAAK-INFORMATIEOBJECTTYPE binnen het ZAAKTYPE."
        ),
    )
    richting = models.CharField(
        _("richting"),
        max_length=20,
        choices=RichtingChoices.choices,
        help_text=_(
            "Aanduiding van de richting van informatieobjecten van het gerelateerde INFORMATIEOBJECTTYPE "
            "bij zaken van het gerelateerde ZAAKTYPE."
        ),
    )

    # this is the relation that is described on StatusType in the specification
    # TODO: validate that statustype is in fact a status type of self.zaaktype
    statustype = models.ForeignKey(
        "datamodel.StatusType",
        verbose_name=_("status type"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="heeft_verplichte_zit",
        help_text=_(
            "URL-referentie naar het STATUSTYPE waarbij deze INFORMATIEOBJECTTYPEn verplicht aanwezig moeten "
            "zijn."
        ),
    )

    class Meta:
        # NOTE: The uniqueness is implied in the specification.
        # unique_together = ("zaaktype", "volgnummer")
        verbose_name = _("Zaak-Informatieobject-Type")
        verbose_name_plural = _("Zaak-Informatieobject-Typen")
        # ordering = unique_together

        filter_fields = ("zaaktype", "informatieobjecttype", "richting")
        ordering_fields = filter_fields
        search_fields = "volgnummer"

    def __str__(self):
        return "{} - {}".format(self.zaaktype, self.volgnummer)


class ZaakInformatieobjectTypeArchiefregime(models.Model):
    """
    ZAAK-INFORMATIETOBJECT-TYPE ARCHIEFREGIME

    Afwijkende archiveringskenmerken van informatieobjecten van een
    INFORMATIEOBJECTTYPE bij zaken van een ZAAKTYPE op grond van
    resultaten van een RESULTAATTYPE bij dat ZAAKTYPE
    """

    zaak_informatieobject_type = models.ForeignKey(
        "datamodel.ZaakInformatieobjectType",
        on_delete=models.CASCADE,
        verbose_name=_("zaakinformatie object type"),
    )
    resultaattype = models.ForeignKey(
        "datamodel.ResultaatType",
        verbose_name=_("resultaattype"),
        on_delete=models.CASCADE,
    )

    # TODO [KING]:  waardenverzameling 'de aanduidingen van de passages cq. klassen in de gehanteerde selectielijst.'
    selectielijstklasse = models.CharField(
        _("selectielijstklasse"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_(
            "Verwijzing naar de voor het ZAAKINFORMATIEOBJECTTYPE bij het RESULTAATTYPE relevante passage in de "
            "Selectielijst Archiefbescheiden van de voor het ZAAKTYPE verantwoordelijke overheidsorganisatie."
        ),
    )
    # choices  Blijvend bewaren Vernietigen
    archiefnominatie = models.CharField(
        _("archiefnominatie"),
        max_length=16,
        choices=ArchiefNominatieChoices.choices,
        help_text=_(
            "Aanduiding die aangeeft of informatieobjecten, van het INFORMATIEOBJECTTYPE bij zaken van het "
            "ZAAKTYPE met een resultaat van het RESULTAATTYPE, blijvend moeten worden bewaard of (op termijn) "
            "moeten worden vernietigd."
        ),
    )
    archiefactietermijn = models.PositiveSmallIntegerField(
        _("archiefactietermijn"),
        validators=[MaxValueValidator(9999)],
        help_text=_(
            "De termijn waarna informatieobjecten, van het INFORMATIEOBJECTTYPE bij zaken van het ZAAKTYPE "
            "met een resultaat van het RESULTAATTYPE, vernietigd of overgebracht (naar een archiefbewaarplaats) "
            "moeten worden."
        ),
    )

    class Meta:
        mnemonic = "ZIA"
        # NOTE: The uniqueness is not explicitly defined in specification:
        unique_together = ("zaak_informatieobject_type", "resultaattype")
        verbose_name = _("Zaak-Informatieobject-Type Archiefregime")
        verbose_name_plural = _("Zaak-Informatieobject-Type Archiefregimes")
        ordering = ("pk",)

        filter_fields = (
            "zaak_informatieobject_type",
            "resultaattype",
            "archiefnominatie",
        )
        ordering_fields = filter_fields
        search_fields = ("selectielijstklasse",)

    def __str__(self):
        return "{} - {}".format("zaak_informatieobject_type", "resultaattype")


class ZaakTypenRelatie(models.Model):
    """
    ZAAKTYPENRELATIE

    Kenmerken van de relatie ZAAKTYPE heeft gerelateerde ZAAKTYPE.
    """

    zaaktype = models.ForeignKey(
        "datamodel.ZaakType",
        verbose_name=_("zaaktype van"),
        related_name="zaaktypenrelaties",
        on_delete=models.CASCADE,
    )

    # TODO: add (shape) validator
    gerelateerd_zaaktype = models.URLField(
        _("gerelateerd zaaktype"),
        help_text=_(
            "URL referentie naar het gerelateerde zaaktype, mogelijks in een extern ZTC."
        ),
    )
    aard_relatie = models.CharField(
        _("aard relatie"),
        max_length=15,
        choices=AardRelatieChoices.choices,
        help_text=_(
            "Omschrijving van de aard van de relatie van zaken van het "
            "ZAAKTYPE tot zaken van het andere ZAAKTYPE"
        ),
    )
    toelichting = models.CharField(
        _("toelichting"),
        max_length=255,
        blank=True,
        help_text=_(
            "Een toelichting op de aard van de relatie tussen beide ZAAKTYPEN."
        ),
    )

    class Meta:
        # NOTE: The uniqueness is not explicitly defined in specification:
        # unique_together = ("zaaktype", "gerelateerd_zaaktype")
        verbose_name = _("Zaaktypenrelatie")
        verbose_name_plural = _("Zaaktypenrelaties")
        ordering = ("pk",)

        filter_fields = ("zaaktype", "gerelateerd_zaaktype", "aard_relatie")
        ordering_fields = filter_fields
        search_fields = ("toelichting",)

    def __str__(self):
        return "{} - {}".format("zaaktype", "gerelateerd_zaaktype")
