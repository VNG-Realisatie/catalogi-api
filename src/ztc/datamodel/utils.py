from datetime import date, datetime, timedelta
from typing import Optional, Union

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q, QuerySet
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import APIException

from ztc.datamodel.models import (
    BesluitType,
    Catalogus,
    Eigenschap,
    InformatieObjectType,
    ResultaatType,
    RolType,
    StatusType,
    ZaakObjectType,
    ZaakType,
)


def get_overlapping_zaaktypes(
    catalogus: Catalogus,
    omschrijving: str,
    begin_geldigheid: date,
    einde_geldigheid: Optional[date] = None,
    instance: Optional[ZaakType] = None,
) -> QuerySet:
    query = ZaakType.objects.filter(
        Q(catalogus=catalogus),
        Q(zaaktype_omschrijving=omschrijving),
        Q(datum_einde_geldigheid=None)
        | Q(datum_einde_geldigheid__gt=begin_geldigheid),  # noqa
    )
    if einde_geldigheid is not None:
        query = query.filter(datum_begin_geldigheid__lte=einde_geldigheid)

    if instance:
        query = query.exclude(pk=instance.pk)

    return query


class OverlappingException(APIException):
    status_code = 400
    default_detail = _(
        f"De object komt al voor binnen de catalogus en opgegeven geldigheidsperiode."
    )
    default_code = "overlapping-geldigheiden"


class TooManyObjectsReturned(APIException):
    status_code = 400
    default_detail = _(
        f"Het is niet mogelijk om te publiseren als hier meerdere objecten worden terug gegeven"
    )
    default_code = "multiple-objects"


def set_geldigheid(
    instance: Optional[Union[ZaakType, BesluitType, InformatieObjectType]]
) -> Optional[Union[ZaakType, BesluitType, InformatieObjectType]]:
    filters = get_filters(instance)

    previous_version = type(instance).objects.filter(**filters)
    if len(previous_version) == 1:
        if (
            previous_version[0].datum_begin_geldigheid
            >= instance.datum_begin_geldigheid
        ):
            raise OverlappingException()

        previous_version[
            0
        ].datum_einde_geldigheid = instance.datum_begin_geldigheid - timedelta(days=1)
        previous_version[0].save()

    elif len(previous_version) == 0:
        pass

    else:
        raise TooManyObjectsReturned()

    # instance.datum_begin_geldigheid = datetime.now().date()
    return instance


def get_relevant_nested_resources(nested_resources) -> dict:
    nested_resources_no_new_zaaktype_on_publish = [
        "informatieobjecttypen",
        "besluittypen",
        "zaaktypenrelaties",
    ]
    for resource in nested_resources_no_new_zaaktype_on_publish:
        del nested_resources[resource]
    return nested_resources


def set_geldigheid_nestled_resources(instance):
    nested_resources = get_relevant_nested_resources(instance._prefetched_objects_cache)

    for resource, new_versions_qs in nested_resources.items():
        for new_version_object in new_versions_qs:
            new_version_object.datum_begin_geldigheid = instance.datum_begin_geldigheid
            new_version_object.save()

            model = apps.get_model(
                app_label="datamodel", model_name=new_version_object._meta.object_name
            )
            filters = get_filters_nested_resources(instance, new_version_object)

            try:
                previous_version = model.objects.filter(**filters).get(
                    ~Q(zaaktype=instance)
                )
                previous_version.datum_einde_geldigheid = (
                    instance.datum_begin_geldigheid - timedelta(days=1)
                )
                previous_version.save()

            except model.DoesNotExist:
                pass


def get_filters(instance) -> dict:
    filters = {"datum_einde_geldigheid": None, "concept": False}

    if isinstance(instance, ZaakType):
        filters["identificatie"] = instance.identificatie
    elif isinstance(instance, InformatieObjectType) or isinstance(
        instance, BesluitType
    ):
        filters["omschrijving"] = instance.omschrijving
    return filters


def get_filters_nested_resources(instance, object) -> dict:
    filters = {
        "datum_einde_geldigheid": None,
        "zaaktype__identificatie": instance.identificatie,
    }
    if isinstance(object, StatusType):
        filters["statustype_omschrijving"] = object.statustype_omschrijving
    elif isinstance(object, RolType) or isinstance(object, ResultaatType):
        filters["omschrijving"] = object.omschrijving
    elif isinstance(object, Eigenschap):
        filters["eigenschapnaam"] = object.eigenschapnaam
    elif isinstance(object, ZaakObjectType):
        filters["objecttype"] = object.objecttype
    return filters
