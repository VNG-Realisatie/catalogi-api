import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from vng_api_common.caching import ETagMixin

from ztc.datamodel.models.mixins import DatumObjectMixin, GeldigheidMixin


class ZaakObjectType(ETagMixin, GeldigheidMixin, DatumObjectMixin):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )

    ander_objecttype = models.BooleanField(
        _("Ander objecttype"),
        help_text=_(
            "Aanduiding waarmee wordt aangegeven of het ZAAKOBJECTTYPE een ander, "
            "niet in RSGB en RGBZ voorkomend, objecttype betreft."
        ),
    )

    objecttype = models.URLField(
        _("Objecttype"),
        help_text=_(
            "URL-referentie naar de OBJECTTYPE waartoe dit ZAAKOBJECTTYPE behoort."
        ),
    )

    relatie_omschrijving = models.CharField(
        _("Relatie omschrijving"),
        max_length=80,
        help_text=_(
            "Omschrijving van de betrekking van het Objecttype op zaken van het gerelateerde ZAAKTYPE."
        ),
    )

    zaaktype = models.ForeignKey(
        "datamodel.ZaakType",
        verbose_name=_("Zaaktype"),
        related_name="objecttypen",
        help_text=_(
            "URL-referentie naar de ZAAKTYPE waartoe dit ZAAKOBJECTTYPE behoort."
        ),
        on_delete=models.CASCADE,
    )

    catalogus = models.ForeignKey(
        "datamodel.Catalogus",
        verbose_name=_("Catalogus"),
        on_delete=models.CASCADE,
        help_text=_(
            "URL-referentie naar de CATALOGUS waartoe dit ZAAKOBJECTTYPE behoort."
        ),
    )

    class Meta:
        verbose_name = _("Zaakobjecttype")
        verbose_name_plural = _("Zaakobjecttypen")
        ordering = ("catalogus", "datum_begin_geldigheid")
