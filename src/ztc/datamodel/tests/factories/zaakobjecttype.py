import factory
import factory.fuzzy

from ztc.datamodel.models.zaakobjecttype import ZaakObjectType

from .catalogus import CatalogusFactory
from .zaken import ZaakTypeFactory


class ZaakObjectTypeFactory(factory.django.DjangoModelFactory):
    datum_begin_geldigheid = factory.Faker("date_this_year")
    relatie_omschrijving = factory.Faker("text", max_nb_chars=40)
    catalogus = factory.SubFactory(CatalogusFactory)
    zaaktype = factory.SubFactory(ZaakTypeFactory)

    ander_objecttype = False

    class Meta:
        model = ZaakObjectType

    @factory.post_generation
    def resultaattypen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for resultaattype in extracted:
                self.resultaattypen.add(resultaattype)

    @factory.post_generation
    def statustypen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for statustype in extracted:
                self.statustypen.add(statustype)
