from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ztc.utils.admin import EditInlineAdminMixin, ListObjectActionsAdminMixin

from ..models import (
    BronCatalogus, BronZaakType, Eigenschap, Formulier, ProductDienst,
    ReferentieProces, ResultaatType, RolType, StatusType, ZaakObjectType,
    ZaakType, ZaakTypenRelatie
)
from .eigenschap import EigenschapAdmin
from .mixins import GeldigheidAdminMixin
from .resultaattype import ResultaatTypeAdmin
from .roltype import RolTypeAdmin
from .statustype import StatusTypeAdmin


@admin.register(ZaakObjectType)
class ZaakObjectTypeAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    list_display = ['objecttype', 'ander_objecttype', 'status_type']
    # list_filter = ('', )
    search_fields = (
        'objecttype',
        'ander_objecttype',
        'relatieomschrijving',
        'status_type',
    )
    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'objecttype',
                'ander_objecttype',
                'relatieomschrijving',
                'status_type',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'is_relevant_voor',
            )
        }),
    )


class StatusTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = StatusType
    fields = StatusTypeAdmin.list_display
    fk_name = 'is_van'


class ZaakObjectTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = ZaakObjectType
    fields = ZaakObjectTypeAdmin.list_display
    fk_name = 'is_relevant_voor'


class RolTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = RolType
    fields = RolTypeAdmin.list_display
    fk_name = 'is_van'


class EigenschapInline(EditInlineAdminMixin, admin.TabularInline):
    model = Eigenschap
    fields = EigenschapAdmin.list_display
    fk_name = 'is_van'


class ResultaatTypeInline(EditInlineAdminMixin, admin.TabularInline):
    model = ResultaatType
    fields = ResultaatTypeAdmin.list_display
    fk_name = 'is_relevant_voor'


class ZaakTypenRelatieInline(admin.TabularInline):
    model = ZaakTypenRelatie
    fk_name = 'zaaktype_van'
    extra = 1


@admin.register(ZaakType)
class ZaakTypeAdmin(ListObjectActionsAdminMixin,GeldigheidAdminMixin, admin.ModelAdmin):
    list_display = ('zaaktype_omschrijving', 'zaakcategorie', 'maakt_deel_uit_van')
    list_filter = ('maakt_deel_uit_van', )
    search_fields = (
        'zaaktype_omschrijving',
        'zaaktype_omschrijving_generiek',
        'zaakcategorie',
        'onderwerp',
        'trefwoord'
    )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'zaaktype_identificatie',
                'zaaktype_omschrijving',
                'zaaktype_omschrijving_generiek',
                'zaakcategorie',
                'doel',
                'aanleiding',
                'toelichting',
                'indicatie_intern_of_extern',
                'handeling_initiator',
                'onderwerp',
                'handeling_behandelaar',
                'doorlooptijd_behandeling',
                'servicenorm_behandeling',
                'opschorting_aanhouding_mogelijk',
                'verlenging_mogelijk',
                'verlengingstermijn',
                'trefwoord',
                'archiefclassificatiecode',
                'vertrouwelijkheidaanduiding',
                'verantwoordelijke',


                'product_dienst',  # m2m
                'formulier',  # m2m

                'verantwoordingsrelatie',
                'versiedatum',  # ??
                'referentieproces',
                'broncatalogus',  #
                'bronzaaktype',  # dit is het model
            )
        }),
        (_('Publicatie'), {
            'fields': (
                'publicatie_indicatie',
                'publicatietekst',
            )
        }),
        (_('Relaties'), {
            'fields': (
                'maakt_deel_uit_van',

                # m2m:
                'is_deelzaaktype_van',
            )
        }),
    )
    inlines = (
        ZaakTypenRelatieInline,  # heeft_gerelateerd
        StatusTypeInline, ZaakObjectTypeInline, RolTypeInline, EigenschapInline, ResultaatTypeInline,
    )

    def get_object_actions(self, obj):
        return (
            (
                _('Toon {}').format(StatusType._meta.verbose_name_plural),
                self._build_changelist_url(StatusType, query={'is_van': obj.pk})
            ),
            (
                _('Toon {}').format(ZaakObjectType._meta.verbose_name_plural),
                self._build_changelist_url(ZaakObjectType, query={'is_relevant_voor': obj.pk})
            ),
            (
                _('Toon {}').format(RolType._meta.verbose_name_plural),
                self._build_changelist_url(RolType, query={'is_van': obj.pk})
            ),
            (
                _('Toon {}').format(Eigenschap._meta.verbose_name_plural),
                self._build_changelist_url(Eigenschap, query={'is_van': obj.pk})
            ),
            (
                _('Toon {}').format(ResultaatType._meta.verbose_name_plural),
                self._build_changelist_url(ResultaatType, query={'is_relevant_voor': obj.pk})
            ),
        )



#
# models for ZaakType
#
@admin.register(ProductDienst)
class ZaakTypeAdmin(admin.ModelAdmin):
    list_display = ['naam']
    fields = ('naam', 'link')


@admin.register(Formulier)
class ZaakTypeAdmin(admin.ModelAdmin):
    list_display = ['naam']
    fields = ('naam', 'link')


@admin.register(ReferentieProces)
class ZaakTypeAdmin(admin.ModelAdmin):
    list_display = ['naam']
    fields = ('naam', 'link')


@admin.register(BronCatalogus)
class ZaakTypeAdmin(admin.ModelAdmin):
    list_display = ['domein', 'rsin']
    fields = ('domein', 'rsin')


@admin.register(BronZaakType)
class ZaakTypeAdmin(admin.ModelAdmin):
    list_display = ['zaaktype_identificatie', 'zaaktype_omschrijving']
    fields = ('zaaktype_identificatie', 'zaaktype_omschrijving')
