from django.test import TestCase

from ztc.datamodel.models import (
    InformatieObjectType, ResultaatType, ZaakInformatieobjectType,
    ZaakInformatieobjectTypeArchiefregime, ZaakType, ZaakTypenRelatie
)

from .factories import (
    BesluitTypeFactory, BronCatalogusFactory, BronZaakTypeFactory,
    CatalogusFactory, CheckListItemFactory, EigenschapFactory,
    EigenschapReferentieFactory, EigenschapSpecificatieFactory,
    FormulierFactory, InformatieObjectTypeFactory,
    InformatieObjectTypeOmschrijvingGeneriekFactory, ProductDienstFactory,
    ReferentieProcesFactory, ResultaatTypeFactory, RolTypeFactory,
    StatusTypeFactory, ZaakObjectTypeFactory, ZaakTypeFactory,
    ZaakTypenRelatieFactory
)


class FactoryTests(TestCase):

    def test_factories(self):
        iot = InformatieObjectTypeFactory.create()

        self.assertIsNotNone(iot.informatieobjecttype_omschrijving_generiek_id)
        self.assertIsNotNone(iot.maakt_deel_uit_van_id)

        iotog = InformatieObjectTypeOmschrijvingGeneriekFactory.create()

        eigenschap_specificatie = EigenschapSpecificatieFactory.create()
        eigenschap_referentie = EigenschapReferentieFactory.create()
        catalogus = CatalogusFactory.create()
        eigenschap = EigenschapFactory.create()
        besluit_type = BesluitTypeFactory.create()
        # self.assertIsNotNone(besluit_type.wordt_vastgelegd_in)
        # self.assertIsNotNone(besluit_type.zaaktypes)
        # self.assertIsNotNone(besluit_type.is_resultaat_van)

        resultaattype = ResultaatTypeFactory.create()
        roltype = RolTypeFactory.create()
        zaakobjecttype = ZaakObjectTypeFactory.create()
        product_dients = ProductDienstFactory.create()
        formulier = FormulierFactory.create()
        referentieproces = ReferentieProcesFactory.create()
        broncatalogus = BronCatalogusFactory.create()
        bronzaaktype = BronZaakTypeFactory.create()
        check_list_item = CheckListItemFactory.create()
        status_type = StatusTypeFactory.create()
        zaaktype = ZaakTypeFactory.create()

    def test_informatie_object_type_factory(self):
        self.assertEqual(InformatieObjectType.objects.count(), 0)
        self.assertEqual(ZaakInformatieobjectType.objects.count(), 0)
        self.assertEqual(ZaakType.objects.count(), 0)

        InformatieObjectTypeFactory.create()

        self.assertEqual(InformatieObjectType.objects.count(), 1)
        self.assertEqual(ZaakInformatieobjectType.objects.count(), 1)
        self.assertEqual(ZaakType.objects.count(), 1)

    def test_zaak_informatieobject_type_archiefregime_factory(self):
        self.assertEqual(ResultaatType.objects.count(), 0)
        self.assertEqual(ZaakInformatieobjectTypeArchiefregime.objects.count(), 0)
        self.assertEqual(ZaakInformatieobjectType.objects.count(), 0)

        resultaattype = ResultaatTypeFactory.create()

        self.assertEqual(ResultaatType.objects.count(), 1)
        self.assertEqual(ZaakInformatieobjectTypeArchiefregime.objects.count(), 1)
        # TODO: we might want to enforce that the same ZIT will be used. they currently belong to different ZaakTypes
        self.assertEqual(ZaakInformatieobjectType.objects.count(), 2)

        resultaattype2 = ResultaatTypeFactory.create(bepaalt_afwijkend_archiefregime_van=None)
        self.assertEqual(ResultaatType.objects.count(), 2)  # + 1
        self.assertEqual(ZaakInformatieobjectTypeArchiefregime.objects.count(), 1)  # stays the same
        self.assertEqual(ZaakInformatieobjectType.objects.count(), 2)  # stay the same

    def test_zaak_typen_relatie_factory(self):
        self.assertEqual(ZaakType.objects.count(), 0)
        self.assertEqual(ZaakTypenRelatie.objects.count(), 0)

        zaaktype1 = ZaakTypeFactory.create()
        zaaktype2 = ZaakTypeFactory.create()

        self.assertEqual(ZaakType.objects.count(), 2)
        self.assertEqual(ZaakTypenRelatie.objects.count(), 0)

        ZaakTypenRelatieFactory.create(
            zaaktype_van=zaaktype1,
            zaaktype_naar=zaaktype2,
        )
        self.assertEqual(ZaakType.objects.count(), 2)
        self.assertEqual(ZaakTypenRelatie.objects.count(), 1)

        self.assertEqual(zaaktype1.heeft_gerelateerd.all().count(), 1)
