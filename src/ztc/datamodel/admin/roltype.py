from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import RolType
from .mixins import FilterSearchOrderingAdminMixin, GeldigheidAdminMixin


@admin.register(RolType)
class RolTypeAdmin(GeldigheidAdminMixin, FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = RolType

    # List
    list_display = ('omschrijving', 'zaaktype')

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'omschrijving',
                'omschrijving_generiek',
                'soort_betrokkene',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'zaaktype',
            )
        }),
    )
    raw_id_fields = ('zaaktype', )
