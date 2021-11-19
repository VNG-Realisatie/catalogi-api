from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import ZaakObjectType
from .mixins import FilterSearchOrderingAdminMixin


@admin.register(ZaakObjectType)
class ZaakObjectTypeAdmin(FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = ZaakObjectType

    # List
    list_display = (
        "ander_objecttype",
        "datum_begin_geldigheid",
        "datum_einde_geldigheid",
        "zaaktype",
        "uuid",
    )

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "uuid",
                    "ander_objecttype",
                    "datum_begin_geldigheid",
                    "datum_einde_geldigheid",
                    "objecttype",
                    "relatie_omschrijving",
                )
            },
        ),
        # zonder inlines aangezien deze erg uitgebreid zouden zijn
        (_("Relaties"), {"fields": ("catalogus", "zaaktype")}),
    )

    readonly_fields = ("uuid",)
    raw_id_fields = ("zaaktype",)
