import factory

from ...models import CheckListItem, StatusType
from .roltype import RolTypeFactory
from .zaken import ZaakTypeFactory


class CheckListItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CheckListItem


class StatusTypeFactory(factory.django.DjangoModelFactory):
    statustypevolgnummer = factory.sequence(lambda n: n + 1)
    zaaktype = factory.SubFactory(ZaakTypeFactory)

    class Meta:
        model = StatusType

    class Params:
        with_etag = factory.Trait(
            _etag=factory.PostGenerationMethodCall("calculate_etag_value")
        )

    @factory.post_generation
    def roltypen(self, create, extracted, **kwargs):
        # optional M2M, do nothing when no arguments are passed
        if not extracted:
            extracted = [RolTypeFactory.create(zaaktype=self.zaaktype)]

        for roltype in extracted:
            self.roltypen.add(roltype)

    @factory.post_generation
    def eigenschappen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for eigenschap in extracted:
                self.eigenschappen.add(eigenschap)

    @factory.post_generation
    def checklistitems(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.checklistitem.add(item)
