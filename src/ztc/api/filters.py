from vng_api_common.filtersets import FilterSet
from django_filters import rest_framework as filters

from ztc.datamodel.models import (
    BesluitType, Eigenschap, InformatieObjectType, ResultaatType, RolType,
    StatusType, ZaakInformatieobjectType, ZaakType
)


# custom filter to show draft and non-drafts
PUBLISH_HELP_TEXT = """filter objects depending on their draft status:
* `all`: show all objects
* `draft`: show only draft or draft-related objects
* `nondraft`: show only non-draft or non-draft-related objects (default)
"""


def publish_filter(queryset, name, value):
    if value == 'draft':
        return queryset.filter(**{name: True})
    elif value == 'nondraft':
        return queryset.filter(**{name: False})
    elif value == 'all':
        return queryset


class RolTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='zaaktype__draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = RolType
        fields = (
            'zaaktype',
            'omschrijving_generiek',
            'publish'
        )


class ZaakInformatieobjectTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='zaaktype__draft', method='publish_filter_m2m', help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = ZaakInformatieobjectType
        fields = (
            'zaaktype',
            'informatie_object_type',
            'richting',
            'publish',
        )

    def publish_filter_m2m(self, queryset, name, value):
        if value == 'draft':
            return queryset.filter(zaaktype__draft=True, informatie_object_type=True)
        elif value == 'nondraft':
            return queryset.filter(zaaktype__draft=False, informatie_object_type=False)
        elif value == 'all':
            return queryset


class ResultaatTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='zaaktype__draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = ResultaatType
        fields = (
            'zaaktype',
            'publish'
        )


class StatusTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='zaaktype__draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = StatusType
        fields = (
            'zaaktype',
            'publish'
        )


class EigenschapFilter(FilterSet):
    publish = filters.CharFilter(field_name='zaaktype__draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = Eigenschap
        fields = (
            'zaaktype',
            'publish'
        )


class ZaakTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = ZaakType
        fields = (
            'catalogus',
            'publish'
        )


class InformatieObjectTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = InformatieObjectType
        fields = (
            'catalogus',
            'publish'
        )


class BesluitTypeFilter(FilterSet):
    publish = filters.CharFilter(field_name='draft', method=publish_filter, help_text=PUBLISH_HELP_TEXT)

    class Meta:
        model = BesluitType
        fields = (
            'catalogus',
            'publish'
        )
