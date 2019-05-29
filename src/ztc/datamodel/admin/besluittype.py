from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .mixins import GeldigheidAdminMixin
from ..models import BesluitType


@admin.register(BesluitType)
class BesluitTypeAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    # List
    list_display = ('catalogus', 'omschrijving', 'besluitcategorie', )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'omschrijving',
                'omschrijving_generiek',
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
                'catalogus',
                'informatieobjecttypes',
                # 'resultaattypes',
                'zaaktypes',
            )
        }),
    )
    filter_horizontal = ('informatieobjecttypes', 'zaaktypes')  # , 'resultaattypes'
