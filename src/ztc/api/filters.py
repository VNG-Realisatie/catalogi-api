from django_filters import rest_framework as filters
from vng_api_common.filtersets import FilterSet

from ztc.datamodel.models import (
    BesluitType, Eigenschap, InformatieObjectType, ResultaatType, RolType,
    StatusType, ZaakInformatieobjectType, ZaakType
)

# custom filter to show concept and non-concepts
STATUS_HELP_TEXT = """filter objects depending on their concept status:
* `alles`: toon objecten waarvan het attribuut `concept` true of false is.
* `concept`: toon objecten waarvan het attribuut `concept` true is.
* `definitief`: toon objecten waarvan het attribuut `concept` false is (standaard).
"""


def status_filter(queryset, name, value):
    if value == 'concept':
        return queryset.filter(**{name: True})
    elif value == 'definitief':
        return queryset.filter(**{name: False})
    elif value == 'alles':
        return queryset


class RolTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='zaaktype__concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = RolType
        fields = (
            'zaaktype',
            'omschrijving_generiek',
            'status'
        )


class ZaakInformatieobjectTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='zaaktype__concept', method='status_filter_m2m', help_text=STATUS_HELP_TEXT)

    class Meta:
        model = ZaakInformatieobjectType
        fields = (
            'zaaktype',
            'informatie_object_type',
            'richting',
            'status',
        )

    def status_filter_m2m(self, queryset, name, value):
        if value == 'concept':
            return queryset.filter(zaaktype__concept=True, informatie_object_type__concept=True)
        elif value == 'definitief':
            return queryset.filter(zaaktype__concept=False, informatie_object_type__concept=False)
        elif value == 'alles':
            return queryset


class ResultaatTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='zaaktype__concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = ResultaatType
        fields = (
            'zaaktype',
            'status'
        )


class StatusTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='zaaktype__concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = StatusType
        fields = (
            'zaaktype',
            'status'
        )


class EigenschapFilter(FilterSet):
    status = filters.CharFilter(field_name='zaaktype__concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = Eigenschap
        fields = (
            'zaaktype',
            'status'
        )


class ZaakTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = ZaakType
        fields = (
            'catalogus',
            'status'
        )


class InformatieObjectTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = InformatieObjectType
        fields = (
            'catalogus',
            'status'
        )


class BesluitTypeFilter(FilterSet):
    status = filters.CharFilter(field_name='concept', method=status_filter, help_text=STATUS_HELP_TEXT)

    class Meta:
        model = BesluitType
        fields = (
            'catalogus',
            'status'
        )
