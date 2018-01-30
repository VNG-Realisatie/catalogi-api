import factory

from ...models import BesluitType
from .catalogus import CatalogusFactory
from .resultaattype import ResultaatTypeFactory
from .zaken import ZaakTypeFactory


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

        dates_begin_geldigheid = []
        for zaak_type in extracted:
            dates_begin_geldigheid.append(
                (zaak_type.datum_begin_geldigheid_date, zaak_type.datum_begin_geldigheid)
            )
            self.zaaktypes.add(zaak_type)

        # sort the list on python datetime.date(), the first element of the tuple, and then
        # use the OnvolledigeDatum value (second element in tuple) as the value
        dates_begin_geldigheid.sort()
        self.datum_begin_geldigheid = dates_begin_geldigheid[0][1]

    @factory.post_generation
    def is_resultaat_van(self, create, extracted, **kwargs):
        # required M2M, if it is not passed in, create one
        if not extracted:
            extracted = [ResultaatTypeFactory.create()]

        for resultaat_type in extracted:
            self.is_resultaat_van.add(resultaat_type)
