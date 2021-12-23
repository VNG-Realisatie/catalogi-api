from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import RolType
from .mixins import FilterSearchOrderingAdminMixin


@admin.register(RolType)
class RolTypeAdmin(FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = RolType

    # List
    list_display = (
        "omschrijving",
        "zaaktype",
        "uuid",
        "catalogus",
    )

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "omschrijving",
                    "omschrijving_generiek",
                    "soort_betrokkene",
                    "datum_begin_geldigheid",
                    "datum_einde_geldigheid",
                )
            },
        ),
        (
            _("Relaties"),
            {
                "fields": (
                    "zaaktype",
                    "catalogus",
                )
            },
        ),
    )
    raw_id_fields = ("zaaktype",)
