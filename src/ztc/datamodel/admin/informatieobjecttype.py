from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ztc.datamodel.models.besluittype import BesluitType

from ..models import (
    InformatieObjectType,
    InformatieObjectTypeOmschrijvingGeneriek,
    ZaakInformatieobjectType,
)
from .mixins import ConceptAdminMixin, GeldigheidAdminMixin


class ZaakInformatieobjectTypeInline(admin.TabularInline):
    model = ZaakInformatieobjectType
    extra = 1
    raw_id_fields = ("zaaktype", "statustype")


class BesluitTypenInline(admin.TabularInline):
    model = BesluitType.informatieobjecttypen.through
    extra = 1


@admin.register(InformatieObjectTypeOmschrijvingGeneriek)
class InformatieObjectTypeOmschrijvingGeneriekAdmin(
    GeldigheidAdminMixin, admin.ModelAdmin
):
    # List
    list_display = ("informatieobjecttype_omschrijving_generiek",)
    search_fields = (
        "informatieobjecttype_omschrijving_generiek",
        "definitie_informatieobjecttype_omschrijving_generiek",
        "herkomst_informatieobjecttype_omschrijving_generiek",
        "hierarchie_informatieobjecttype_omschrijving_generiek",
        "opmerking_informatieobjecttype_omschrijving_generiek",
    )

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "informatieobjecttype_omschrijving_generiek",
                    "definitie_informatieobjecttype_omschrijving_generiek",
                    "herkomst_informatieobjecttype_omschrijving_generiek",
                    "hierarchie_informatieobjecttype_omschrijving_generiek",
                    "opmerking_informatieobjecttype_omschrijving_generiek",
                )
            },
        ),
    )


@admin.register(InformatieObjectType)
class InformatieObjectTypeAdmin(
    GeldigheidAdminMixin, ConceptAdminMixin, admin.ModelAdmin
):
    list_display = (
        "catalogus",
        "omschrijving",
        "informatieobjectcategorie",
        "uuid",
        "get_absolute_api_url",
    )
    list_filter = ("catalogus", "informatieobjectcategorie")
    search_fields = (
        "omschrijving",
        "informatieobjectcategorie",
        "trefwoord",
        "toelichting",
        "uuid",
    )
    ordering = ("catalogus", "omschrijving")

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {
                "fields": (
                    "uuid",
                    "omschrijving",
                    "informatieobjectcategorie",
                    "trefwoord",
                    "vertrouwelijkheidaanduiding",
                    "model",
                    "toelichting",
                )
            },
        ),
        (
            _("Relaties"),
            {
                "fields": (
                    "catalogus",
                    "omschrijving_generiek",
                )
            },
        ),
    )
    filter_horizontal = ("besluittypen",)
    readonly_fields = ("uuid",)
    inlines = (
        BesluitTypenInline,
        # ZaakInformatieobjectTypeInline,
    )  # zaaktypes
