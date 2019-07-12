from rest_framework import mixins, viewsets

from ...datamodel.models import ZaakType
from ..filters import ZaakTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import ZaakTypeSerializer
from .mixins import ConceptMixin, M2MConceptCreateMixin

# class ZaakObjectTypeViewSet(NestedViewSetMixin, FilterSearchOrderingViewSetMixin,
#                             FlexFieldsMixin, viewsets.ReadOnlyModelViewSet):
#     """
#     retrieve:
#     De objecttypen van objecten waarop een zaak van het ZAAKTYPE betrekking kan hebben.
#
#     list:
#     Een verzameling van ZAAKOBJECTTYPEn.
#     """
#     queryset = ZaakObjectType.objects.all()
#     serializer_class = ZaakObjectTypeSerializer
#
#     required_scopes = {
#         'list': SCOPE_ZAAKTYPES_READ,
#         'retrieve': SCOPE_ZAAKTYPES_READ,
#
#     }


class ZaakTypeViewSet(ConceptMixin,
                      M2MConceptCreateMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Het geheel van karakteristieke eigenschappen van zaken van eenzelfde soort.

    list:
    Een verzameling van ZAAKTYPEn.
    """
    queryset = ZaakType.objects.prefetch_related(
        'statustypen',
        'zaaktypenrelaties',
        'heeft_relevant_informatieobjecttype',
        'statustypen',
        'resultaattypen',
        'eigenschap_set',
        'roltype_set',
        'besluittype_set',
    ).order_by('-pk')
    serializer_class = ZaakTypeSerializer
    lookup_field = 'uuid'
    filterset_class = ZaakTypeFilter
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
        'publish': SCOPE_ZAAKTYPES_WRITE,
    }
    concept_related_fields = ['besluittype_set']
