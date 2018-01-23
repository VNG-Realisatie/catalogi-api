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
    is_van = factory.SubFactory(ZaakTypeFactory)

    class Meta:
        model = Eigenschap
