from datetime import date, datetime, timedelta
from typing import Optional

from rest_framework.exceptions import APIException

from django.apps import apps
from django.db.models import Q, QuerySet
from django.utils.translation import ugettext_lazy as _

from ztc.datamodel.models import (
    Eigenschap,
    StatusType,
    ResultaatType,
    RolType,
    ZaakObjectType,
    ZaakType,
    Catalogus,
    BesluitType,
    InformatieObjectType,
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


def set_geldigheid(instance):
    filters = get_filters(instance)
    previous_version = type(instance).objects.filter(**filters)
    if previous_version:
        if not previous_version[0].datum_begin_geldigheid < datetime.now().date():
            message = _(
                f"Dit {type(instance).__name__} komt al voor binnen de catalogus en opgegeven geldigheidsperiode."
            )
            raise APIException(message, code="overlapping")
        previous_version[0].datum_einde_geldigheid = datetime.now().date() - timedelta(
            days=1
        )
        previous_version[0].save()

    instance.datum_begin_geldigheid = datetime.now().date()
    return instance


def set_geldigheid_nestled_resources(instance):
    nested_resources = instance._prefetched_objects_cache
    del nested_resources["informatieobjecttypen"]
    del nested_resources["besluittypen"]
    for resource, new_versions_qs in nested_resources.items():
        for new_version_object in new_versions_qs:
            new_version_object.datum_begin_geldigheid = datetime.now().date()
            new_version_object.save()

            model = apps.get_model(
                app_label="datamodel", model_name=new_version_object._meta.object_name
            )
            filters = get_filters_nested_resources(instance, model, new_version_object)
            previous_version = model.objects.filter(**filters).exclude(
                Q(zaaktype=instance)
            )
            if previous_version:
                previous_version[
                    0
                ].datum_einde_geldigheid = datetime.now().date() - timedelta(days=1)
                previous_version[0].save()


def get_filters(instance):
    filters = {"datum_einde_geldigheid": None, "concept": False}
    if isinstance(instance, ZaakType):
        filters["identificatie"] = instance.identificatie
    elif isinstance(instance, InformatieObjectType) or isinstance(
        instance, BesluitType
    ):
        filters["omschrijving"] = (instance.omschrijving,)
        filters["omschrijving"] = filters["omschrijving"][0]
    return filters


def get_filters_nested_resources(instance, model, object):
    filters = {
        "datum_einde_geldigheid": None,
        "zaaktype_identificatie": instance.identificatie,
    }
    if isinstance(model, StatusType):
        filters["statustype_omschrijving"] = object.statustype_omschrijving
    elif isinstance(model, RolType) or isinstance(model, ResultaatType):
        filters["omschrijving"] = object.omschrijving
    elif isinstance(model, Eigenschap):
        filters["eigenschapnaam"] = object.eigenschapnaam
    elif isinstance(model, ZaakObjectType):
        filters["objecttype"] = object.objecttype

    return filters
