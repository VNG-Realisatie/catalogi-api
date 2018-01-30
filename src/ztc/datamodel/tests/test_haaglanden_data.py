from django.test import TestCase

from ztc.datamodel.tests.base_tests import HaaglandenMixin

from ..models import Catalogus, ZaakType


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
