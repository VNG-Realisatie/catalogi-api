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
    eigenschapnaam = factory.Sequence(lambda n: 'eigenschap {}'.format(n))
    is_van = factory.SubFactory(ZaakTypeFactory)
    datum_begin_geldigheid = factory.SelfAttribute('is_van.datum_begin_geldigheid')

    class Meta:
        model = Eigenschap
