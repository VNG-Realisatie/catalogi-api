from datetime import date

from django.test import TestCase

from freezegun import freeze_time

from ztc.datamodel.tests.base_tests import HaaglandenMixin

from ..models import (
    BesluitType,
    Catalogus,
    CheckListItem,
    Eigenschap,
    EigenschapReferentie,
    EigenschapSpecificatie,
    InformatieObjectType,
    InformatieObjectTypeOmschrijvingGeneriek,
    ResultaatType,
    RolType,
    StatusType,
    ZaakType,
)


@freeze_time("2018-01-30")
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
        self.assertEqual(
            InformatieObjectTypeOmschrijvingGeneriek.objects.all().count(), 2
        )
        self.assertEqual(InformatieObjectType.objects.all().count(), 2)
        self.assertEqual(ResultaatType.objects.all().count(), 5)
        self.assertEqual(RolType.objects.all().count(), 7)
        self.assertEqual(StatusType.objects.all().count(), 5)

        self.assertEqual(CheckListItem.objects.all().count(), 0)
        self.assertEqual(EigenschapReferentie.objects.all().count(), 0)
        self.assertEqual(EigenschapSpecificatie.objects.all().count(), 2)

        #
        # now test the datum_begin_geldigheid on all instances, duplicate code so the default error msg makes sense
        #
        expected_dates = [
            date(2018, 1, 30)
        ]  # since the freeze time is used, that date should appear
        self.assertEqual(
            list(
                set(
                    BesluitType.objects.values_list("datum_begin_geldigheid", flat=True)
                )
            ),
            expected_dates,
        )
