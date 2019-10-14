from datetime import date, timedelta

import factory

from ...models import BesluitType
from .catalogus import CatalogusFactory
from .resultaattype import ResultaatTypeFactory
from .zaken import ZaakTypeFactory


class BesluitTypeFactory(factory.django.DjangoModelFactory):
    omschrijving = "Besluittype"
    catalogus = factory.SubFactory(CatalogusFactory)
    reactietermijn = timedelta(days=14)
    publicatie_indicatie = False
    datum_begin_geldigheid = date(2018, 1, 1)

    class Meta:
        model = BesluitType

    class Params:
        with_etag = factory.Trait(
            _etag=factory.PostGenerationMethodCall("calculate_etag_value")
        )

    @factory.post_generation
    def informatieobjecttypes(self, create, extracted, **kwargs):
        # optional M2M, do nothing when no arguments are passed
        if not create:
            return

        if extracted:
            for informatieobjecttype in extracted:
                self.informatieobjecttypes.add(informatieobjecttype)

    @factory.post_generation
    def zaaktypes(self, create, extracted, **kwargs):
        # required M2M, if it is not passed in, create one
        if not extracted:
            extracted = [ZaakTypeFactory.create(catalogus=self.catalogus)]

        dates_begin_geldigheid = []
        for zaak_type in extracted:
            dates_begin_geldigheid.append(zaak_type.datum_begin_geldigheid)
            self.zaaktypes.add(zaak_type)

        # sort the list on python datetime.date(), the first element of the tuple, and then
        # use the OnvolledigeDatum value (second element in tuple) as the value
        dates_begin_geldigheid.sort()
        self.datum_begin_geldigheid = dates_begin_geldigheid[0]

    @factory.post_generation
    def resultaattypes(self, create, extracted, **kwargs):
        # required M2M, if it is not passed in, create one
        if not extracted:
            extracted = [ResultaatTypeFactory.create(zaaktype=self.zaaktypes.get())]

        for resultaat_type in extracted:
            self.resultaattypes.add(resultaat_type)
