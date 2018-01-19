import factory

from .catalogus import CatalogusFactory
from .zaken import ZaakTypeFactory
from .resultaattype import ResultaatTypeFactory
from ...models import BesluitType


class BesluitTypeFactory(factory.django.DjangoModelFactory):
    besluittype_omschrijving = 'Besluittype'
    maakt_deel_uit_van = factory.SubFactory(CatalogusFactory)
    reactietermijn = 14

    class Meta:
        model = BesluitType

    @factory.post_generation
    def wordt_vastgelegd_in(self, create, extracted, **kwargs):
        # optional M2M, do nothing when no arguments are passed
        if not create:
            return

        if extracted:
            for informatie_object_type in extracted:
                self.wordt_vastgelegd_in.add(informatie_object_type)

    @factory.post_generation
    def zaaktypes(self, create, extracted, **kwargs):
        # required M2M, if it is not passed in, create one
        if not extracted:
            extracted = [ZaakTypeFactory.create()]

        for zaak_type in extracted:
            self.zaaktypes.add(zaak_type)

    @factory.post_generation
    def is_resultaat_van(self, create, extracted, **kwargs):
        # required M2M, if it is not passed in, create one
        if not extracted:
            extracted = [ResultaatTypeFactory.create()]

        for resultaat_type in extracted:
            self.is_resultaat_van.add(resultaat_type)
