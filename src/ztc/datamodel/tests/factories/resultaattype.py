import factory
import factory.fuzzy
from dateutil.relativedelta import relativedelta

from .zaken import ZaakTypeFactory
from ...models import ResultaatType


class ResultaatTypeFactory(factory.django.DjangoModelFactory):
    zaaktype = factory.SubFactory(ZaakTypeFactory)
    omschrijving = factory.Faker('word', locale='nl')
    resultaattypeomschrijving = factory.Faker('url')
    omschrijving_generiek = factory.Faker('word')
    selectielijstklasse = factory.Faker('url')
    archiefnominatie = factory.fuzzy.FuzzyChoice(['blijvend_bewaren', 'vernietigen'])
    archiefactietermijn = relativedelta(years=10)

    datum_begin_geldigheid = factory.SelfAttribute('zaaktype.datum_begin_geldigheid')

    class Meta:
        model = ResultaatType
