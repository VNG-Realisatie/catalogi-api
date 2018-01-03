from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ...utils.admin import EditInlineAdminMixin, ListObjectActionsAdminMixin
from ..models import BesluitType, Catalogus, InformatieObjectType
from .besluittype import BesluitTypeAdmin
from .informatieobjecttype import InformatieObjectTypeAdmin


class BesluitTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = BesluitType
    fields = BesluitTypeAdmin.list_display
    fk_name = 'maakt_deel_uit_van'


class InformatieObjectTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = InformatieObjectType
    fields = InformatieObjectTypeAdmin.list_display
    fk_name = 'maakt_deel_uit_van'


@admin.register(Catalogus)
class CatalogusAdmin(ListObjectActionsAdminMixin, admin.ModelAdmin):
    # List
    list_display = ('domein', 'rsin', )
    list_filter = ('rsin', )
    search_fields = (
        'domein',
        'rsin',
        'contactpersoon_beheer_naam',
    )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'domein',
                'rsin',
            )
        }),
        (_('Contactpersoon beheer'), {
            'fields': (
                'contactpersoon_beheer_naam',
                'contactpersoon_beheer_telefoonnummer',
                'contactpersoon_beheer_emailadres',
            )
        }),
    )
    inlines = (
        BesluitTypeInline, InformatieObjectTypeInline,
    )

    def get_object_actions(self, obj):
        return (
            (
                _('Toon {}').format(BesluitType._meta.verbose_name_plural),
                self._build_changelist_url(BesluitType, query={'maakt_deel_uit_van': obj.pk})
            ),
            (
                _('Toon {}').format(InformatieObjectType._meta.verbose_name_plural),
                self._build_changelist_url(InformatieObjectType, query={'maakt_deel_uit_van': obj.pk})
            ),
        )
