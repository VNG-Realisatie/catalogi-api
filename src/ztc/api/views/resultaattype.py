from rest_framework import mixins, viewsets
from vng_api_common.viewsets import CheckQueryParamsMixin

from ...datamodel.models import ResultaatType
from ..filters import ResultaatTypeFilter
from ..scopes import SCOPE_ZAAKTYPES_READ, SCOPE_ZAAKTYPES_WRITE
from ..serializers import ResultaatTypeSerializer
from .mixins import ZaakTypeConceptMixin


class ResultaatTypeViewSet(CheckQueryParamsMixin,
                           ZaakTypeConceptMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.ReadOnlyModelViewSet):
    """
    Opvragen en bewerken van RESULTAATTYPEn van een ZAAKTYPE.

    Het betreft de indeling of groepering van resultaten van zaken van hetzelfde
    ZAAKTYPE naar hun aard, zoals 'verleend', 'geweigerd', 'verwerkt', etc.

    create:
    Maak een RESULTAATTYPE aan.

    Maak een RESULTAATTYPE aan. Dit kan alleen als het bijbehorende ZAAKTYPE een
    concept betreft.

    list:
    Alle RESULTAATTYPEn opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke RESULTAATTYPE opvragen.

    Een specifieke RESULTAATTYPE opvragen.

    update:
    Werk een RESULTAATTYPE in zijn geheel bij.

    Werk een RESULTAATTYPE in zijn geheel bij. Dit kan alleen als het
    bijbehorende ZAAKTYPE een concept betreft.

    partial_update:
    Werk een RESULTAATTYPE deels bij.

    Werk een RESULTAATTYPE deels bij. Dit kan alleen als het bijbehorende
    ZAAKTYPE een concept betreft.

    destroy:
    Verwijder een RESULTAATTYPE.

    Verwijder een RESULTAATTYPE. Dit kan alleen als het bijbehorende ZAAKTYPE
    een concept betreft.
    """
    queryset = ResultaatType.objects.all().order_by('-pk')
    serializer_class = ResultaatTypeSerializer
    filter_class = ResultaatTypeFilter
    lookup_field = 'uuid'
    required_scopes = {
        'list': SCOPE_ZAAKTYPES_READ,
        'retrieve': SCOPE_ZAAKTYPES_READ,
        'create': SCOPE_ZAAKTYPES_WRITE,
        'destroy': SCOPE_ZAAKTYPES_WRITE,
    }
