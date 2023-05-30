from urllib.parse import urlparse

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_filters import rest_framework as filters
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_resource_for_path

from ztc.datamodel.models import (
    BesluitType,
    Catalogus,
    Eigenschap,
    InformatieObjectType,
    ResultaatType,
    RolType,
    StatusType,
    ZaakInformatieobjectType,
    ZaakType,
)
from ztc.datamodel.models.zaakobjecttype import ZaakObjectType

# custom filter to show concept and non-concepts
STATUS_HELP_TEXT = """filter objects depending on their concept status:
* `alles`: Toon objecten waarvan het attribuut `concept` true of false is.
* `concept`: Toon objecten waarvan het attribuut `concept` true is.
* `definitief`: Toon objecten waarvan het attribuut `concept` false is (standaard).
"""

DATUM_GELDIGHEID_HELP_TEXT = "filter objecten op hun geldigheids datum."


def get_objects_between_geldigheid_dates(queryset, name, value, *args, **kwargs):
    qs_old_version = queryset.filter(
        datum_begin_geldigheid__lte=value, datum_einde_geldigheid__gte=value
    )
    if not qs_old_version:
        qs_most_recent_version = queryset.filter(datum_einde_geldigheid=None)
        return qs_most_recent_version
    return qs_old_version


def detail_filter(queryset, name, value):
    """filtering is handled in the viewset"""
    return queryset


def status_filter(queryset, name, value):
    if value == "concept":
        return queryset.filter(**{name: True})
    elif value == "definitief":
        return queryset.filter(**{name: False})
    elif value == "alles":
        return queryset


def m2m_filter(queryset, name, value):
    parsed = urlparse(value)
    path = parsed.path
    try:
        object = get_resource_for_path(path)
    except ObjectDoesNotExist:
        return queryset.none()
    return queryset.filter(**{name: object})


class CharArrayFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RolTypeFilter(FilterSet):
    status = filters.CharFilter(
        field_name="zaaktype__concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )
    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    zaaktype_identificatie = filters.CharFilter(field_name="zaaktype__identificatie")

    class Meta:
        model = RolType
        fields = (
            "zaaktype",
            "zaaktype_identificatie",
            "omschrijving_generiek",
            "status",
            "datum_geldigheid",
        )


class ZaakInformatieobjectTypeFilter(FilterSet):
    status = filters.CharFilter(
        field_name="zaaktype__concept",
        method="status_filter_m2m",
        help_text=STATUS_HELP_TEXT,
    )

    class Meta:
        model = ZaakInformatieobjectType
        fields = ("zaaktype", "informatieobjecttype", "richting", "status")

    def status_filter_m2m(self, queryset, name, value):
        if value == "concept":
            return queryset.filter(
                models.Q(zaaktype__concept=True)
                | models.Q(informatieobjecttype__concept=True)
            )
        elif value == "definitief":
            return queryset.filter(
                zaaktype__concept=False, informatieobjecttype__concept=False
            )
        elif value == "alles":
            return queryset


class ResultaatTypeFilter(FilterSet):
    status = filters.CharFilter(
        field_name="zaaktype__concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )

    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    zaaktype_identificatie = filters.CharFilter(field_name="zaaktype__identificatie")

    class Meta:
        model = ResultaatType
        fields = ("zaaktype", "zaaktype_identificatie", "status", "datum_geldigheid")


class StatusTypeFilter(FilterSet):
    status = filters.CharFilter(
        field_name="zaaktype__concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )
    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    zaaktype_identificatie = filters.CharFilter(field_name="zaaktype__identificatie")

    class Meta:
        model = StatusType
        fields = ("zaaktype", "zaaktype_identificatie", "status", "datum_geldigheid")


class EigenschapFilter(FilterSet):
    status = filters.CharFilter(
        field_name="zaaktype__concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )
    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    zaaktype_identificatie = filters.CharFilter(field_name="zaaktype__identificatie")

    class Meta:
        model = Eigenschap
        fields = ("zaaktype", "zaaktype_identificatie", "status", "datum_geldigheid")


class ZaakTypeFilter(FilterSet):
    status = filters.CharFilter(
        field_name="concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )
    trefwoorden = CharArrayFilter(field_name="trefwoorden", lookup_expr="contains")

    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    class Meta:
        model = ZaakType
        fields = (
            "catalogus",
            "identificatie",
            "trefwoorden",
            "status",
            "datum_geldigheid",
        )


class ZaakTypeDetailFilter(FilterSet):
    datum_geldigheid = filters.DateFilter(
        method=detail_filter,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    class Meta:
        model = ZaakType
        fields = ("datum_geldigheid",)


class ZaakObjectTypeFilter(FilterSet):
    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )
    zaaktype_identificatie = filters.CharFilter(field_name="zaaktype__identificatie")

    class Meta:
        model = ZaakObjectType
        fields = (
            "ander_objecttype",
            "catalogus",
            "datum_begin_geldigheid",
            "datum_einde_geldigheid",
            "datum_geldigheid",
            "objecttype",
            "relatie_omschrijving",
            "zaaktype",
            "zaaktype_identificatie",
        )


class InformatieObjectTypeFilter(FilterSet):
    status = filters.CharFilter(
        field_name="concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )
    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    class Meta:
        model = InformatieObjectType
        fields = ("catalogus", "status", "datum_geldigheid", "omschrijving")


class BesluitTypeFilter(FilterSet):
    datum_geldigheid = filters.DateFilter(
        method=get_objects_between_geldigheid_dates,
        help_text=DATUM_GELDIGHEID_HELP_TEXT,
    )

    zaaktypen = filters.CharFilter(
        field_name="zaaktypen",
        method=m2m_filter,
        help_text=_(
            "ZAAKTYPE met ZAAKen die relevant kunnen zijn voor dit BESLUITTYPE"
        ),
        validators=[URLValidator()],
    )
    informatieobjecttypen = filters.CharFilter(
        field_name="informatieobjecttypen",
        method=m2m_filter,
        help_text=_(
            "Het INFORMATIEOBJECTTYPE van informatieobjecten waarin besluiten van dit "
            "BESLUITTYPE worden vastgelegd."
        ),
        validators=[URLValidator()],
    )
    status = filters.CharFilter(
        field_name="concept", method=status_filter, help_text=STATUS_HELP_TEXT
    )

    class Meta:
        model = BesluitType
        fields = (
            "catalogus",
            "zaaktypen",
            "informatieobjecttypen",
            "status",
            "omschrijving",
            "datum_geldigheid",
        )


class CatalogusFilter(FilterSet):
    class Meta:
        model = Catalogus
        fields = {"domein": ["exact", "in"], "rsin": ["exact", "in"]}
