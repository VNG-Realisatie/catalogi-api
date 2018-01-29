from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import CheckListItem, StatusType
from .mixins import GeldigheidAdminMixin


@admin.register(CheckListItem)
class CheckListItemAdmin(admin.ModelAdmin):
    list_display = ('itemnaam',)
    fields = ('itemnaam', 'vraagstelling', 'verplicht', 'toelichting')


@admin.register(StatusType)
class StatusTypeAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    list_display = ('statustype_omschrijving', 'statustypevolgnummer', 'is_van')
    list_filter = ('is_van', )
    search_fields = (
        'statustype_omschrijving', 'statustypevolgnummer'
    )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'statustype_omschrijving',
                'statustype_omschrijving_generiek',
                'statustypevolgnummer',
                'doorlooptijd_status',
                'informeren',
                'statustekst',
                'toelichting',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'is_van',
                'checklistitem',
                'roltypen',
            )
        }),
    )
