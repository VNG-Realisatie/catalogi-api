from datetime import date, timedelta

import factory

from ztc.datamodel.models import (
    BronCatalogus, BronZaakType, Formulier, ProductDienst, ReferentieProces,
    ZaakObjectType, ZaakType
)

from .catalogus import CatalogusFactory
from .relatieklassen import ZaakTypenRelatieFactory  # noqa

ZAAKTYPEN = [
    'Melding behandelen',
    'Toetsing uitvoeren',
    'Vergunningaanvraag regulier behandelen',
    'Vergunningaanvraag uitgebreid behandelen',
    'Vooroverleg voeren',
    'Zienswijze behandelen',
    'Bestuursdwang ten uitvoer leggen',
    'Handhavingsbesluit nemen',
    'Handhavingsverzoek behandelen',
    'Last onder dwangsom ten uitvoer leggen',
    'Toezicht uitvoeren',
    'Advies verstrekken',
    'Beroep behandelen',
    'Bezwaar behandelen',
    'Incidentmelding behandelen',
    'Voorlopige voorziening behandelen',
]


class ProductDienstFactory(factory.django.DjangoModelFactory):
    naam = factory.Sequence(lambda n: 'ProductDienst {}'.format(n))

    class Meta:
        model = ProductDienst


class FormulierFactory(factory.django.DjangoModelFactory):
    naam = factory.Sequence(lambda n: 'Formulier {}'.format(n))

    class Meta:
        model = Formulier


class ReferentieProcesFactory(factory.django.DjangoModelFactory):
    naam = factory.Sequence(lambda n: 'ReferentieProces {}'.format(n))

    class Meta:
        model = ReferentieProces


class BronCatalogusFactory(factory.django.DjangoModelFactory):
    domein = factory.Sequence(lambda n: chr((n % 26) + 65) * 5)  # AAAAA, BBBBB, etc. Repeat after ZZZZZ
    rsin = factory.Sequence(lambda n: '{}'.format(n + 100000000))  # charfield, that is 9 digit number

    class Meta:
        model = BronCatalogus


class BronZaakTypeFactory(factory.django.DjangoModelFactory):
    zaaktype_identificatie = factory.Sequence(lambda n: n)

    class Meta:
        model = BronZaakType


class ZaakTypeFactory(factory.django.DjangoModelFactory):
    zaaktype_identificatie = factory.Sequence(lambda n: n)
    doorlooptijd_behandeling = timedelta(days=30)
    verlengingstermijn = 30
    trefwoord = []  # ArrayField has blank=True but not null=True
    verantwoordingsrelatie = []  # ArrayField has blank=True but not null=True
    catalogus = factory.SubFactory(CatalogusFactory)
    referentieproces = factory.SubFactory(ReferentieProcesFactory)

    datum_begin_geldigheid = date(2018, 1, 1)
    versiedatum = date(2018, 1, 1)

    # this one is optional, if its added as below, it will keep adding related ZaakTypes (and reach max recursion depth)
    # heeft_gerelateerd = factory.RelatedFactory(ZaakTypenRelatieFactory, 'zaaktype_van')

    class Meta:
        model = ZaakType

    @factory.post_generation
    def is_deelzaaktype_van(self, create, extracted, **kwargs):
        # optional M2M, do nothing when no arguments are passed
        if not create:
            return

        if extracted:
            for zaaktype in extracted:
                self.is_deelzaaktype_van.add(zaaktype)

    @factory.post_generation
    def product_dienst(self, create, extracted, **kwargs):
        # required M2M
        if not extracted:
            extracted = [ProductDienstFactory.create()]

        for product_dienst in extracted:
            self.product_dienst.add(product_dienst)


class ZaakObjectTypeFactory(factory.django.DjangoModelFactory):
    is_relevant_voor = factory.SubFactory(ZaakTypeFactory)
    datum_begin_geldigheid = factory.SelfAttribute('is_relevant_voor.datum_begin_geldigheid')

    class Meta:
        model = ZaakObjectType
