from django.urls import reverse

from zds_schema.constants import RolOmschrijvingGeneriek

from ...datamodel.tests.factories import RolTypeFactory
from .base import APITestCase


class RolTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.rol_type = RolTypeFactory.create(
            omschrijving='Vergunningaanvrager',
            omschrijving_generiek=RolOmschrijvingGeneriek.initiator,
            soort_betrokkene=['Aanvrager'],
            zaaktype__maakt_deel_uit_van=self.catalogus,
        )
        self.zaaktype = self.rol_type.zaaktype

        self.rol_type_list_url = reverse('roltype-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_uuid': self.catalogus.uuid,
            'zaaktype_uuid': self.zaaktype.uuid
        })
        self.rol_type_detail_url = reverse('roltype-detail', kwargs={
            'version': self.API_VERSION,
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
            'omschrijvingGeneriek': RolOmschrijvingGeneriek.initiator,
            'mogelijkeBetrokkenen': [],
            # 'soortBetrokkene': ['Aanvrager'],
            # 'magZetten': [],
        }
        self.assertEqual(expected, response.json())

    def test_mag_zetten(self):
        pass
