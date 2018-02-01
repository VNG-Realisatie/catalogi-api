import factory

from ...models import RolType
from .zaken import ZaakTypeFactory


class RolTypeFactory(factory.django.DjangoModelFactory):
    soort_betrokkene = ['soort betrokkene']
    is_van = factory.SubFactory(ZaakTypeFactory)
    datum_begin_geldigheid = factory.SelfAttribute('is_van.datum_begin_geldigheid')

    class Meta:
        model = RolType
