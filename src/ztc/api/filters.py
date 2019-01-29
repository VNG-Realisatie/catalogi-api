from zds_schema.filtersets import FilterSet

from ztc.datamodel.models import RolType, ZaakInformatieobjectType


class RolTypeFilter(FilterSet):
    class Meta:
        model = RolType
        fields = (
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
