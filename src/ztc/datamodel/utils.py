from datetime import date
from typing import Optional

from django.db.models import Q, QuerySet

from ztc.datamodel.models import Catalogus, ZaakType


def get_overlapping_zaaktypes(
    catalogus: Catalogus,
    identificatie: str,
    begin_geldigheid: date,
    einde_geldigheid: Optional[date] = None,
    instance: Optional[ZaakType] = None,
) -> QuerySet:
    query = ZaakType.objects.filter(
        Q(catalogus=catalogus),
        Q(identificatie=identificatie),
        Q(datum_einde_geldigheid=None)
        | Q(datum_einde_geldigheid__gt=begin_geldigheid),  # noqa
    )
    if einde_geldigheid is not None:
        query = query.filter(datum_begin_geldigheid__lte=einde_geldigheid)

    if instance:
        query = query.exclude(pk=instance.pk)

    return query

