from vng_api_common.filtersets import FilterSet

from ztc.datamodel.models import (
    BesluitType, Eigenschap, InformatieObjectType, ResultaatType, RolType,
    StatusType, ZaakInformatieobjectType, ZaakType
)


class RolTypeFilter(FilterSet):
    class Meta:
        model = RolType
        fields = (
            'zaaktype',
            'omschrijving_generiek',
        )


class ZaakInformatieobjectTypeFilter(FilterSet):
    class Meta:
        model = ZaakInformatieobjectType
        fields = (
            'zaaktype',
            'informatie_object_type',
            'richting',
        )


class ResultaatTypeFilter(FilterSet):
    class Meta:
        model = ResultaatType
        fields = (
            'zaaktype',
        )


class StatusTypeFilter(FilterSet):
    class Meta:
        model = StatusType
        fields = (
            'zaaktype',
        )


class EigenschapFilter(FilterSet):
    class Meta:
        model = Eigenschap
        fields = (
            'zaaktype',
        )


class ZaakTypeFilter(FilterSet):
    class Meta:
        model = ZaakType
        fields = (
            'catalogus',
        )


class InformatieObjectTypeFilter(FilterSet):
    class Meta:
        model = InformatieObjectType
        fields = (
            'catalogus',
        )


class BesluitTypeFilter(FilterSet):
    class Meta:
        model = BesluitType
        fields = (
            'catalogus',
        )
