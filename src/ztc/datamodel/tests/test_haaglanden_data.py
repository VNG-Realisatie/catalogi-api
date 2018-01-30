from django.test import TestCase

from ztc.datamodel.tests.base_tests import HaaglandenMixin

from ..models import (
    BesluitType, BronCatalogus, BronZaakType, Catalogus, CheckListItem,
    Eigenschap, EigenschapReferentie, EigenschapSpecificatie, Formulier,
    InformatieObjectType, InformatieObjectTypeOmschrijvingGeneriek,
    ProductDienst, ReferentieProces, ResultaatType, RolType, StatusType,
    ZaakObjectType, ZaakType
)


class FactoryTests(HaaglandenMixin, TestCase):

    def test_haaglanden_data_setup(self):
        """
        The Haaglanden base test should create
        - 1 Catalogus
        - 1 Zaaktype
        etc.

        And not many extra Catalogi/ZaakTypes through all the subfactories.
        """
        self.assertEqual(Catalogus.objects.all().count(), 1)
        self.assertEqual(ZaakType.objects.all().count(), 1)
        self.assertEqual(BesluitType.objects.all().count(), 4)
        self.assertEqual(Eigenschap.objects.all().count(), 2)
        self.assertEqual(InformatieObjectTypeOmschrijvingGeneriek.objects.all().count(), 2)
        self.assertEqual(InformatieObjectType.objects.all().count(), 2)
        self.assertEqual(ProductDienst.objects.all().count(), 1)
        self.assertEqual(ReferentieProces.objects.all().count(), 1)
        self.assertEqual(ResultaatType.objects.all().count(), 5)
        self.assertEqual(RolType.objects.all().count(), 7)
        self.assertEqual(StatusType.objects.all().count(), 5)
        self.assertEqual(ZaakObjectType.objects.all().count(), 3)

        self.assertEqual(BronCatalogus.objects.all().count(), 0)
        self.assertEqual(BronZaakType.objects.all().count(), 0)
        self.assertEqual(CheckListItem.objects.all().count(), 0)
        self.assertEqual(EigenschapReferentie.objects.all().count(), 0)
        self.assertEqual(EigenschapSpecificatie.objects.all().count(), 0)
        self.assertEqual(Formulier.objects.all().count(), 0)
