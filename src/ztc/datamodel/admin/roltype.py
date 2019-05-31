from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .mixins import FilterSearchOrderingAdminMixin, GeldigheidAdminMixin
from ..models import MogelijkeBetrokkene, RolType


class MogelijkeBetrokkeneInline(admin.TabularInline):
    model = MogelijkeBetrokkene
    readonly_fields = ('uuid',)
    extra = 1


@admin.register(RolType)
class RolTypeAdmin(GeldigheidAdminMixin, FilterSearchOrderingAdminMixin, admin.ModelAdmin):
    model = RolType

    # List
    list_display = ('omschrijving', 'zaaktype', 'uuid')

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

    inlines = [MogelijkeBetrokkeneInline]
