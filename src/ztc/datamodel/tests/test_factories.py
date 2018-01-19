from django.test import TestCase

from .factories import (
    CatalogusFactory,
    ZaakTypeFactory, BesluitTypeFactory,
    InformatieObjectTypeFactory, EigenschapFactory,
    EigenschapReferentieFactory, EigenschapSpecificatieFactory,
    InformatieObjectTypeOmschrijvingGeneriekFactory,
    ResultaatTypeFactory,
    RolTypeFactory, CheckListItemFactory,
    StatusTypeFactory, ZaakObjectTypeFactory,
    ProductDienstFactory, FormulierFactory, ReferentieProcesFactory,
    BronCatalogusFactory, BronZaakTypeFactory,
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
