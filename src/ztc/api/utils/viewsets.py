import uuid
from datetime import timedelta
from typing import Optional, Union
from urllib.parse import urlparse

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


def is_url(pattern: str):
    is_url = urlparse(pattern)
    return all([is_url.scheme, is_url.netloc])


def build_absolute_url(action, request):
    if action in ["update", "partial_update"]:
        return request.build_absolute_uri().rsplit("/", 2)[0]
    return request.build_absolute_uri().rsplit("/", 1)[0]


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

    elif len(previous_version) > 1:
        raise TooManyObjectsReturned()

    return instance


def get_relevant_nested_resources(nested_resources) -> dict:
    nested_resources_no_new_zaaktype_on_publish = [
        "informatieobjecttypen",
        "besluittypen",
        "zaaktypenrelaties",
    ]

    for resource in nested_resources_no_new_zaaktype_on_publish:
        if resource in nested_resources:
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

            previous_version = model.objects.filter(**filters).filter(
                ~Q(zaaktype=instance)
            )
            if len(previous_version) == 1:
                previous_version[
                    0
                ].datum_einde_geldigheid = instance.datum_begin_geldigheid - timedelta(
                    days=1
                )
                previous_version[0].save()

            elif len(previous_version) > 1:
                raise TooManyObjectsReturned()


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


def m2m_array_of_str_to_url(request, m2m_field: str, m2m_model, action: str):
    """
    The m2m array 'm2m_field' (like 'besluittypen') is transformed to an array of urls, which are required for the
    m2m relationship.
    """
    m2m_data = request.data.get(m2m_field, []).copy()
    request.data[m2m_field].clear()
    for m2m_str in m2m_data:
        search_parameter = (
            Q(omschrijving=m2m_str)
            if m2m_model == BesluitType
            else Q(identificatie=m2m_str)
        )
        m2m_objects = m2m_model.objects.filter(
            get_m2m_filters(request.data.get("begin_geldigheid")) & search_parameter
        )

        for m2m_object in m2m_objects:
            request.data[m2m_field].extend(
                [
                    f"{build_absolute_url(action, request)}/{m2m_field}/{str(m2m_object.uuid)}"
                ]
            )
    return request


def remove_invalid_m2m(serializer, m2m_field: str, m2m_model, action: str):
    data = serializer.data if action == "list" else [serializer.data]
    for query_object in data:
        valid_urls = []
        for m2m_url in query_object[m2m_field]:
            uuid_from_url = uuid.UUID(m2m_url.rsplit("/", 1)[1]).hex
            valid_m2m = m2m_model.objects.filter(
                Q(uuid=uuid_from_url)
                & get_m2m_filters(query_object["begin_geldigheid"])
                & Q(concept=False)
            )
            if valid_m2m:
                valid_urls.append(m2m_url)

        query_object[m2m_field].clear()
        query_object[m2m_field].extend(valid_urls)

    return serializer


def get_m2m_filters(search_object):
    return Q(datum_begin_geldigheid__lte=search_object) & Q(
        datum_einde_geldigheid__gte=search_object
    ) | Q(datum_begin_geldigheid__lte=search_object) & Q(datum_einde_geldigheid=None)
