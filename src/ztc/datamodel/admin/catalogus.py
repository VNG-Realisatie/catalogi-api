from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ...utils.admin import EditInlineAdminMixin, ListObjectActionsAdminMixin
from ..models import BesluitType, Catalogus, InformatieObjectType, ZaakType
from .besluittype import BesluitTypeAdmin
from .informatieobjecttype import InformatieObjectTypeAdmin
from .mixins import FilterSearchOrderingAdminMixin
from .zaken import ZaakTypeAdmin


class ZaakTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = ZaakType
    fields = ZaakTypeAdmin.list_display
    fk_name = "catalogus"


class BesluitTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = BesluitType
    fields = BesluitTypeAdmin.list_display


class InformatieObjectTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = InformatieObjectType
    fields = InformatieObjectTypeAdmin.list_display
    fk_name = "catalogus"


@admin.register(Catalogus)
class CatalogusAdmin(
    ListObjectActionsAdminMixin, FilterSearchOrderingAdminMixin, admin.ModelAdmin
):
    model = Catalogus

    # List
    list_display = ("naam", "versie", "domein", "rsin", "uuid")

    # Details
    fieldsets = (
        (
            _("Algemeen"),
            {"fields": ("naam", "versie", "datum_begin_versie", "domein", "rsin")},
        ),
        (
            _("Contactpersoon beheer"),
            {
                "fields": (
                    "contactpersoon_beheer_naam",
                    "contactpersoon_beheer_telefoonnummer",
                    "contactpersoon_beheer_emailadres",
                )
            },
        ),
    )
    inlines = (ZaakTypeInline, BesluitTypeInline, InformatieObjectTypeInline)

    def get_object_actions(self, obj):
        return (
            (
                _("Toon {}").format(ZaakType._meta.verbose_name_plural),
                self._build_changelist_url(ZaakType, query={"catalogus": obj.pk}),
            ),
            (
                _("Toon {}").format(BesluitType._meta.verbose_name_plural),
                self._build_changelist_url(BesluitType, query={"catalogus": obj.pk}),
            ),
            (
                _("Toon {}").format(InformatieObjectType._meta.verbose_name_plural),
                self._build_changelist_url(
                    InformatieObjectType, query={"catalogus": obj.pk}
                ),
            ),
        )
