from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import RolType
from .mixins import GeldigheidAdminMixin


@admin.register(RolType)
class RolTypeAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    list_display = ('roltypeomschrijving', 'is_van')
    list_filter = ('is_van', )
    search_fields = ('roltypeomschrijving',)

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
