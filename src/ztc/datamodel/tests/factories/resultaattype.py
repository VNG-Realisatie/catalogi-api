import factory

from ztc.datamodel.choices import ArchiefProcedure

from ...models import ResultaatType
from .relatieklassen import ZaakInformatieobjectTypeArchiefregimeFactory
from .zaken import ZaakTypeFactory


class ResultaatTypeFactory(factory.django.DjangoModelFactory):
    resultaattypeomschrijving = 'omschrijving'
    brondatum_archiefprocedure = ArchiefProcedure.eigenschap
    archiefactietermijn = 14
    is_relevant_voor = factory.SubFactory(ZaakTypeFactory)

    # call this factory with bepaalt_afwijkend_archiefregime_van = None when you dont want it
    bepaalt_afwijkend_archiefregime_van = factory.RelatedFactory(
        ZaakInformatieobjectTypeArchiefregimeFactory, 'resultaattype')

    datum_begin_geldigheid = factory.SelfAttribute('is_relevant_voor.datum_begin_geldigheid')

    class Meta:
        model = ResultaatType
