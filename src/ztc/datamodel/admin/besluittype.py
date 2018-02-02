from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import BesluitType
from .mixins import FilterSearchOrderingAdminMixin, GeldigheidAdminMixin


@admin.register(BesluitType)
class BesluitTypeAdmin(GeldigheidAdminMixin, FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = BesluitType

    # List
    list_display = ('maakt_deel_uit_van', 'besluittype_omschrijving', 'besluitcategorie', )

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
