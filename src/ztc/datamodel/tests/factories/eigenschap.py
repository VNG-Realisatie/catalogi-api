import factory

from ...models import Eigenschap, EigenschapReferentie, EigenschapSpecificatie
from .zaken import ZaakTypeFactory


class EigenschapSpecificatieFactory(factory.django.DjangoModelFactory):
    waardenverzameling = []  # ArrayField has blank=True but not null=True

    class Meta:
        model = EigenschapSpecificatie


class EigenschapReferentieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EigenschapReferentie


class EigenschapFactory(factory.django.DjangoModelFactory):
    eigenschapnaam = factory.Sequence(lambda n: "eigenschap {}".format(n))
    zaaktype = factory.SubFactory(ZaakTypeFactory)
    specificatie_van_eigenschap = factory.SubFactory(EigenschapSpecificatieFactory)

    datum_begin_geldigheid = factory.Faker("date_this_decade")

    class Meta:
        model = Eigenschap

    class Params:
        with_etag = factory.Trait(
            _etag=factory.PostGenerationMethodCall("calculate_etag_value")
        )
