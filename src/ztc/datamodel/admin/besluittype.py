from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import BesluitType
from .mixins import GeldigheidAdminMixin


@admin.register(BesluitType)
class BesluitTypeAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    # List
    list_display = ('maakt_deel_uit_van', 'besluittype_omschrijving', 'besluitcategorie', )
    list_filter = ('maakt_deel_uit_van', )
    search_fields = (
        'besluittype_omschrijving',
        'besluittype_omschrijving_generiek',
        'besluitcategorie',
        'toelichting',
        'publicatietekst',
    )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'besluittype_omschrijving',
                'besluittype_omschrijving_generiek',
                'besluitcategorie',
                'reactietermijn',
                'toelichting',
            )
        }),
        (_('Publicatie'), {
            'fields': (
                'publicatie_indicatie',
                'publicatietekst',
                'publicatietermijn',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'maakt_deel_uit_van',
                'wordt_vastgelegd_in',
            )
        }),
    )
    filter_horizontal = ('wordt_vastgelegd_in', )
