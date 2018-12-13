from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import (
    InformatieObjectType, InformatieObjectTypeOmschrijvingGeneriek,
    ZaakInformatieobjectType
)
from .mixins import FilterSearchOrderingAdminMixin, GeldigheidAdminMixin


class ZaakInformatieobjectTypeInline(admin.TabularInline):
    model = ZaakInformatieobjectType
    extra = 1
    raw_id_fields = ('zaaktype', 'status_type', )


@admin.register(InformatieObjectTypeOmschrijvingGeneriek)
class InformatieObjectTypeOmschrijvingGeneriekAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    # List
    list_display = ('informatieobjecttype_omschrijving_generiek', )
    search_fields = (
        'informatieobjecttype_omschrijving_generiek',
        'definitie_informatieobjecttype_omschrijving_generiek',
        'herkomst_informatieobjecttype_omschrijving_generiek',
        'hierarchie_informatieobjecttype_omschrijving_generiek',
        'opmerking_informatieobjecttype_omschrijving_generiek',
    )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'informatieobjecttype_omschrijving_generiek',
                'definitie_informatieobjecttype_omschrijving_generiek',
                'herkomst_informatieobjecttype_omschrijving_generiek',
                'hierarchie_informatieobjecttype_omschrijving_generiek',
                'opmerking_informatieobjecttype_omschrijving_generiek',
            )
        }),
    )


@admin.register(InformatieObjectType)
class InformatieObjectTypeAdmin(GeldigheidAdminMixin, FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = InformatieObjectType

    # List
    list_display = ('catalogus', 'informatieobjecttype_omschrijving', 'informatieobjectcategorie', )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'informatieobjecttype_omschrijving',
                'informatieobjectcategorie',
                'informatieobjecttypetrefwoord',
                'vertrouwelijkheidaanduiding',
                'model',
                'toelichting',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'catalogus',
                'informatieobjecttype_omschrijving_generiek',
            )
        }),
    )
    inlines = (ZaakInformatieobjectTypeInline, )  # zaaktypes
