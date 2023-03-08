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
        m2m_objects = m2m_model.objects.filter(search_parameter)

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
                & Q(datum_einde_geldigheid=None)
                & Q(concept=False)
            )
            if valid_m2m:
                valid_urls.append(m2m_url)

        query_object[m2m_field].clear()
        query_object[m2m_field].extend(valid_urls)

    return
