import factory

from ztc.datamodel.choices import RichtingChoices

from ...models import (
    ZaakInformatieobjectType,
    ZaakInformatieobjectTypeArchiefregime,
    ZaakTypenRelatie,
)


class ZaakInformatieobjectTypeFactory(factory.django.DjangoModelFactory):
    zaaktype = factory.SubFactory("ztc.datamodel.tests.factories.ZaakTypeFactory")
    informatieobjecttype = factory.SubFactory(
        "ztc.datamodel.tests.factories.InformatieObjectTypeFactory", zaaktypes=None
    )
    volgnummer = factory.sequence(lambda x: x)
    richting = RichtingChoices.inkomend

    class Meta:
        model = ZaakInformatieobjectType


class ZaakInformatieobjectTypeArchiefregimeFactory(factory.django.DjangoModelFactory):
    zaak_informatieobject_type = factory.SubFactory(ZaakInformatieobjectTypeFactory)
    resultaattype = factory.SubFactory(
        "ztc.datamodel.tests.factories.ResultaatTypeFactory"
    )
    archiefactietermijn = 7

    class Meta:
        model = ZaakInformatieobjectTypeArchiefregime


class ZaakTypenRelatieFactory(factory.django.DjangoModelFactory):
    zaaktype = factory.SubFactory("ztc.datamodel.tests.factories.ZaakTypeFactory")
    gerelateerd_zaaktype = factory.Faker("url")

    class Meta:
        model = ZaakTypenRelatie
