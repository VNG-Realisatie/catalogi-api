from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import ResultaatType, ZaakInformatieobjectTypeArchiefregime
from .forms import ResultaatTypeForm
from .mixins import GeldigheidAdminMixin


class ZaakInformatieobjectTypeArchiefregimeInline(admin.TabularInline):
    model = ZaakInformatieobjectTypeArchiefregime
    extra = 1


@admin.register(ResultaatType)
class ResultaatTypeAdmin(GeldigheidAdminMixin, admin.ModelAdmin):
    model = ResultaatType
    form = ResultaatTypeForm

    # List
    list_display = ('omschrijving', 'omschrijving_generiek', 'selectielijstklasse', 'uuid')
    ordering = ('zaaktype', 'omschrijving')
    search_fields = (
        'omschrijving',
        'omschrijving_generiek',
        'selectielijstklasse',
        'toelichting',
        'uuid',
    )

    # Details
    fieldsets = (
        (_('Algemeen'), {
            'fields': (
                'zaaktype',
                'omschrijving',
                'toelichting',
            )
        }),
        (_('Gemeentelijke selectielijst'), {
            'fields': (
                'resultaattypeomschrijving',
                'selectielijstklasse',
            )
        }),
        (_('Bepaling brondatum archiefprocedure'), {
            'fields': (
                'brondatum_archiefprocedure_afleidingswijze',
                'brondatum_archiefprocedure_datumkenmerk',
                'brondatum_archiefprocedure_einddatum_bekend',
                'brondatum_archiefprocedure_objecttype',
                'brondatum_archiefprocedure_registratie',
                'brondatum_archiefprocedure_procestermijn',
            ),
        }),
        # (_('Relaties'), {
        #     'fields': (
        #         'heeft_verplichte_zot',
        #         'heeft_verplichte_ziot'
        #     )
        # }),
    )
    raw_id_fields = ('zaaktype',)
