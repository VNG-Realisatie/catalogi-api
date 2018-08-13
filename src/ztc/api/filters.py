from zds_schema.filtersets import FilterSet

from ztc.datamodel.models import RolType


class RolTypeFilter(FilterSet):
    class Meta:
        model = RolType
        fields = (
            'omschrijving_generiek',
        )
