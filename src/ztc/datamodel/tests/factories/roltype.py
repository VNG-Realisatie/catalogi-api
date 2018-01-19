import factory

from ...models import RolType
from .zaken import ZaakTypeFactory


class RolTypeFactory(factory.django.DjangoModelFactory):
    soort_betrokkene = ['soort betrokkene']
    is_van = factory.SubFactory(ZaakTypeFactory)

    class Meta:
        model = RolType
