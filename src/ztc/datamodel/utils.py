from datetime import date, datetime, timedelta
from typing import Optional, Union

from django.apps import apps
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


def set_geldigheid(
    instance: Optional[Union[ZaakType, BesluitType, InformatieObjectType]]
) -> Optional[Union[ZaakType, BesluitType, InformatieObjectType]]:
    filters = get_filters(instance)
    try:
        previous_version = type(instance).objects.get(**filters)
        if not previous_version.datum_begin_geldigheid < datetime.now().date():
            message = _(
                f"Dit {type(instance).__name__} komt al voor binnen de catalogus en opgegeven geldigheidsperiode."
            )
            raise APIException(message, code="overlapping")
        previous_version.datum_einde_geldigheid = datetime.now().date() - timedelta(
            days=1
        )
        previous_version.save()

    except type(instance).DoesNotExist:
        pass

    instance.datum_begin_geldigheid = datetime.now().date()
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
            new_version_object.datum_begin_geldigheid = datetime.now().date()
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
                    datetime.now().date() - timedelta(days=1)
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
