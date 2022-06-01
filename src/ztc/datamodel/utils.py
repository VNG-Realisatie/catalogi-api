from datetime import date, datetime, timedelta
from typing import Optional

from rest_framework.exceptions import APIException

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


def set_geldigheid_zaaktype(instance):
    previous_version = ZaakType.objects.filter(
        datum_einde_geldigheid=None, identificatie=instance.identificatie
    )
    if previous_version:

        if not previous_version[0].datum_begin_geldigheid < datetime.now().date():
            message = _(
                "Dit zaaktype komt al voor binnen de catalogus en opgegeven geldigheidsperiode."
            )
            raise APIException(message, code="overlapping")
        previous_version[0].datum_einde_geldigheid = datetime.now().date() - timedelta(
            days=1
        )
        previous_version[0].save()

    instance.datum_begin_geldigheid = datetime.now().date()
    return instance


def set_geldigheid_nestled_resources(instance):
    for resource in [
        RolType,
        StatusType,
        Eigenschap,
        ZaakObjectType,
        ResultaatType,
    ]:
        current_version = resource.objects.filter(
            datum_einde_geldigheid=None,
            zaaktype_identificatie=instance.identificatie,
            zaaktype=instance,
        )
        if current_version:
            current_version[0].datum_begin_geldigheid = datetime.now().date()
            current_version[0].save()

            previous_version = resource.objects.filter(
                datum_einde_geldigheid=None,
                zaaktype_identificatie=instance.identificatie,
            ).exclude(zaaktype=instance)
            if previous_version:
                previous_version[
                    0
                ].datum_einde_geldigheid = datetime.now().date() - timedelta(days=1)
                previous_version[0].save()
