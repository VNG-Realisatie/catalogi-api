from datetime import timedelta
from typing import Optional, Union

from django.apps import apps
from django.db.models import Q

from ztc.api.utils.exceptions import OverlappingException, TooManyObjectsReturned
from ztc.datamodel.models import (
    BesluitType,
    Eigenschap,
    InformatieObjectType,
    ResultaatType,
    RolType,
    StatusType,
    ZaakObjectType,
    ZaakType,
)


class FilterSearchOrderingViewSetMixin(object):
    """
    Consult the model options to set filter-, ordering- and search fields.
    """

    def get_model_option(self, attr, default=None):
        if default is None:
            default = []
        return getattr(self.queryset.model._meta, attr, default)

    @property
    def filter_fields(self):
        """
        The fields that can be used as query param, to filter the results.
        """
        return self.get_filter_fields()

    @property
    def ordering_fields(self):
        """
        The fields that can be used in the query param ``?ordering=``
        """
        return self.get_ordering_fields()

    @property
    def search_fields(self):
        """
        The fields that can be used in the query param ``?search=``
        """
        return self.get_search_fields()

    def get_filter_fields(self):
        """
        This function can be overriden to return custom fields.
        """
        return self.get_model_option("filter_fields")

    def get_ordering_fields(self):
        """
        This function can be overriden to return custom fields.
        """
        return self.get_model_option("ordering_fields")

    def get_search_fields(self):
        """
        This function can be overriden to return custom fields.
        """
        return self.get_model_option("search_fields")


def set_geldigheid(
    instance: Union[ZaakType, BesluitType, InformatieObjectType]
) -> Union[ZaakType, BesluitType, InformatieObjectType]:
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
