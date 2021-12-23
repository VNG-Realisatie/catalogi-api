from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import Eigenschap, EigenschapReferentie, EigenschapSpecificatie
from .mixins import FilterSearchOrderingAdminMixin


@admin.register(Eigenschap)
class EigenschapAdmin(FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = Eigenschap

    # List
    list_display = ("eigenschapnaam", "zaaktype", "statustype")

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "eigenschapnaam",
                    "definitie",
                    "toelichting",
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
                    "statustype",
                    "specificatie_van_eigenschap",
                    "referentie_naar_eigenschap",
                )
            },
        ),
    )


@admin.register(EigenschapReferentie)
class EigenschapReferentieAdmin(admin.ModelAdmin):
    # List
    list_display = ("objecttype", "informatiemodel")  # Add is_van
    # list_filter = ('rsin', )  # Add is_van
    search_fields = (
        "objecttype",
        "informatiemodel",
        "namespace",
        "schemalocatie",
        "x_path_element",
        "entiteittype",
    )

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "objecttype",
                    "informatiemodel",
                    "namespace",
                    "schemalocatie",
                    "x_path_element",
                    "entiteittype",
                )
            },
        ),
    )


@admin.register(EigenschapSpecificatie)
class EigenschapSpecificatieAdmin(admin.ModelAdmin):
    # List
    list_display = ("groep", "formaat", "lengte", "kardinaliteit")  # Add is_van
    # list_filter = ('rsin', )  # Add is_van
    search_fields = ("groep",)

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "groep",
                    "formaat",
                    "lengte",
                    "kardinaliteit",
                    "waardenverzameling",
                )
            },
        ),
    )
