from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import RolType
from .mixins import FilterSearchOrderingAdminMixin, GeldigheidAdminMixin


@admin.register(RolType)
class RolTypeAdmin(GeldigheidAdminMixin, FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = RolType

    # List
    list_display = ('roltypeomschrijving', 'is_van')

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'roltypeomschrijving',
                'roltypeomschrijving_generiek',
                'soort_betrokkene',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'is_van',
            )
        }),
    )
    raw_id_fields = ('is_van', )
