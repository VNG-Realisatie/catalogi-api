import factory

from ztc.datamodel.choices import ArchiefProcedure
from ...models import ResultaatType
from .zaken import ZaakTypeFactory


class ResultaatTypeFactory(factory.django.DjangoModelFactory):
    resultaattypeomschrijving = 'omschrijving'
    brondatum_archiefprocedure = ArchiefProcedure.eigenschap
    archiefactietermijn = 14
    is_relevant_voor = factory.SubFactory(ZaakTypeFactory)

    class Meta:
        model = ResultaatType
