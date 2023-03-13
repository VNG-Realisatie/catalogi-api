from ztc.datamodel.models import (
    BesluitType,
    InformatieObjectType,
    ZaakType,
)
import uuid

from urllib.parse import urlparse
from django.db.models import Q


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


MAPPING_FIELD_TO_MODEL = {
    "zaaktypen": ZaakType,
    "deelzaaktypen": ZaakType,
    "gerelateerde_zaaktypen": ZaakType,
    "besluittypen": BesluitType,
    "informatieobjecttypen": InformatieObjectType,

}


def m2m_array_of_str_to_url(request, m2m_fields: list, action: str):
    """
    The m2m array 'm2m_field' (like 'besluittypen') is transformed to an array of urls, which are required for the
    m2m relationship.
    """

    for m2m_field in m2m_fields:
        m2m_data = request.data.get(m2m_field, []).copy()
        if m2m_data:
            request.data[m2m_field].clear()

        for m2m_str in m2m_data:
            search_parameter = (
                Q(omschrijving=m2m_str)
                if MAPPING_FIELD_TO_MODEL[m2m_field] in [BesluitType, InformatieObjectType]
                else Q(identificatie=m2m_str if m2m_field != "gerelateerde_zaaktypen" else m2m_str["zaaktype"])
            )

            m2m_objects = MAPPING_FIELD_TO_MODEL[m2m_field].objects.filter(search_parameter)
            for m2m_object in m2m_objects:
                if m2m_field == "gerelateerde_zaaktypen":
                    new_m2m_str = m2m_str.copy()
                    new_m2m_str.update({
                                       "zaaktype": f"{build_absolute_url(action, request)}/{MAPPING_FIELD_TO_MODEL[m2m_field]._meta.verbose_name_plural.title().lower()}/{str(m2m_object.uuid)}"})
                    request.data[m2m_field].extend([new_m2m_str])
                else:
                    request.data[m2m_field].extend(
                        [
                            f"{build_absolute_url(action, request)}/{MAPPING_FIELD_TO_MODEL[m2m_field]._meta.verbose_name_plural.title().lower()}/{str(m2m_object.uuid)}"
                        ]
                    )

    return request


def remove_invalid_m2m(serializer, m2m_fields: list, action: str):
    for m2m_field in m2m_fields:
        data = serializer.data if action == "list" else [serializer.data]
        for query_object in data:
            valid_urls = []
            for m2m_url in query_object[m2m_field]:
                uuid_from_url = uuid.UUID(m2m_url.rsplit("/", 1)[1]).hex

                valid_m2m = MAPPING_FIELD_TO_MODEL[m2m_field].objects.filter(
                    Q(uuid=uuid_from_url)
                    & get_m2m_filters(query_object["begin_geldigheid"], query_object["einde_geldigheid"])
                    & Q(concept=False)
                )

                if valid_m2m:
                    valid_urls.append(m2m_url)

            query_object[m2m_field].clear()
            query_object[m2m_field].extend(valid_urls)

    return serializer


def get_m2m_filters(start, end):
    # search_params = Q(datum_begin_geldigheid__lte=start) & Q(
    #     datum_einde_geldigheid__gte=start
    # ) | Q(datum_begin_geldigheid__lte=start) & Q(datum_einde_geldigheid=None)
    if end:
        return Q(datum_begin_geldigheid__lte=end) & Q(
            datum_einde_geldigheid__gte=start
        )
    else:
        return Q(datum_begin_geldigheid__gte=start)  # todo or return Q(datum_einde_geldigheid=None) ?
