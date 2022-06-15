import factory
import factory.fuzzy
from dateutil.relativedelta import relativedelta

from ...models import ResultaatType
from .zaken import ZaakTypeFactory


class ResultaatTypeFactory(factory.django.DjangoModelFactory):
    zaaktype = factory.SubFactory(ZaakTypeFactory)
    omschrijving = factory.Faker("word", locale="nl")
    resultaattypeomschrijving = factory.Faker("url")
    omschrijving_generiek = factory.Faker("word")
    selectielijstklasse = factory.Faker("url")
    archiefnominatie = factory.fuzzy.FuzzyChoice(["blijvend_bewaren", "vernietigen"])
    archiefactietermijn = relativedelta(years=10)

    @factory.post_generation
    def besluittypen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for besluittype in extracted:
                self.besluittype_set.add(besluittype)

    @factory.post_generation
    def informatieobjecttypen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for informatieobjecttype in extracted:
                self.informatieobjecttypen.add(informatieobjecttype)

    class Meta:
        model = ResultaatType

    class Params:
        with_etag = factory.Trait(
            _etag=factory.PostGenerationMethodCall("calculate_etag_value")
        )
