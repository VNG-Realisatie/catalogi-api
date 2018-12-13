import uuid

from rest_framework import status
from zds_schema.constants import RolOmschrijving

from ...datamodel.tests.factories import RolTypeFactory
from .base import APITestCase
from .utils import reverse


class RolTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.rol_type = RolTypeFactory.create(
            omschrijving='Vergunningaanvrager',
            omschrijving_generiek=RolOmschrijving.initiator,
            soort_betrokkene=['Aanvrager'],
            zaaktype__catalogus=self.catalogus,
        )
        self.zaaktype = self.rol_type.zaaktype

        self.rol_type_list_url = reverse('roltype-list', kwargs={
            'catalogus_uuid': self.catalogus.uuid,
            'zaaktype_uuid': self.zaaktype.uuid
        })
        self.rol_type_detail_url = reverse('roltype-detail', kwargs={
            'catalogus_uuid': self.catalogus.uuid,
            'zaaktype_uuid': self.zaaktype.uuid,
            'uuid': self.rol_type.uuid,
        })

    def test_get_list(self):
        response = self.api_client.get(self.rol_type_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # TODO: when pagination gets re-added
        # self.assertTrue('results' in data)
        # self.assertEqual(len(data['results']), 1)
        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.rol_type_detail_url)
        self.assertEqual(response.status_code, 200)

        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_uuid': self.catalogus.uuid,
            'uuid': self.zaaktype.uuid,
        })

        expected = {
            'url': f'http://testserver{self.rol_type_detail_url}',
            # 'ingangsdatumObject': '2018-01-01',
            # 'einddatumObject': None,
            'zaaktype': f'http://testserver{zaaktype_url}',
            'omschrijving': 'Vergunningaanvrager',
            'omschrijvingGeneriek': RolOmschrijving.initiator,
            'mogelijkeBetrokkenen': [],
            # 'soortBetrokkene': ['Aanvrager'],
            # 'magZetten': [],
        }
        self.assertEqual(expected, response.json())

    def test_mag_zetten(self):
        pass


class FilterValidationTests(APITestCase):

    def test_invalid_filters(self):
        url = reverse('roltype-list', kwargs={
            'catalogus_uuid': str(uuid.uuid4()),
            'zaaktype_uuid': str(uuid.uuid4()),
        })

        invalid_filters = {
            'omschrijvingGeneriek': 'invalid-option',  # bestaat niet
            'foo': 'bar',  # unsupported param
        }

        for key, value in invalid_filters.items():
            with self.subTest(query_param=key, value=value):
                response = self.client.get(url, {key: value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
