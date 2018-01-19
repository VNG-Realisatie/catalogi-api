import factory

from ...models import CheckListItem, StatusType
from .zaken import ZaakTypeFactory
from .roltype import RolTypeFactory


class CheckListItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CheckListItem


class StatusTypeFactory(factory.django.DjangoModelFactory):
    statustypevolgnummer = factory.sequence(lambda n: n + 1)
    is_van = factory.SubFactory(ZaakTypeFactory)

    class Meta:
        model = StatusType

    @factory.post_generation
    def roltypen(self, create, extracted, **kwargs):
        # optional M2M, do nothing when no arguments are passed
        if not extracted:
            extracted = [RolTypeFactory.create()]

        for roltype in extracted:
            self.roltypen.add(roltype)
