from unittest import skip

from django.urls import reverse

from ...datamodel.choices import RolTypeOmschrijving
from ...datamodel.tests.factories import RolTypeFactory
from .base import APITestCase


@skip("Not MVP yet")
class RolTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.rol_type = RolTypeFactory.create(
            roltypeomschrijving='Vergunningaanvrager',
            roltypeomschrijving_generiek=RolTypeOmschrijving.initiator,
            soort_betrokkene=['Aanvrager'],
            is_van__maakt_deel_uit_van=self.catalogus,
        )
        self.zaaktype = self.rol_type.is_van

        self.rol_type_list_url = reverse('api:roltype-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.rol_type_detail_url = reverse('api:roltype-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.rol_type.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.rol_type_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.rol_type_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver{}'.format(self.rol_type_detail_url),
            'ingangsdatumObject': '2018-01-01',
            'einddatumObject': None,
            'isVan': 'http://testserver{}'.format(
                reverse('api:zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk])),
            'omschrijving': 'Vergunningaanvrager',
            'omschrijvingGeneriek': 'Initiator',
            'soortBetrokkene': ['Aanvrager'],
            'magZetten': [],
        }
        self.assertEqual(expected, response.json())

    def test_mag_zetten(self):
        pass
