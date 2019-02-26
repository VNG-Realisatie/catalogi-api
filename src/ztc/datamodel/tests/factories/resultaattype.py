from datetime import timedelta

import factory
import factory.fuzzy

from ...models import ResultaatType
from .zaken import ZaakTypeFactory

TEN_YEARS = 10 * 365


class ResultaatTypeFactory(factory.django.DjangoModelFactory):
    zaaktype = factory.SubFactory(ZaakTypeFactory)
    omschrijving = factory.Faker('word', locale='nl')
    resultaattypeomschrijving = factory.Faker('url')
    omschrijving_generiek = factory.Faker('word')
    selectielijstklasse = factory.Faker('url')
    archiefnominatie = factory.fuzzy.FuzzyChoice(['blijvend_bewaren', 'vernietigen'])
    archiefactietermijn = timedelta(days=TEN_YEARS)

    datum_begin_geldigheid = factory.SelfAttribute('zaaktype.datum_begin_geldigheid')

    class Meta:
        model = ResultaatType
