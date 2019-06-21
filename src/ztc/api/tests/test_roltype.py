from rest_framework import status
from vng_api_common.constants import RolOmschrijving

from ...datamodel.tests.factories import RolTypeFactory, ZaakTypeFactory
from ...datamodel.models import RolType
from .base import APITestCase
from .utils import reverse


class RolTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        RolTypeFactory.create(
            omschrijving='Vergunningaanvrager',
            omschrijving_generiek=RolOmschrijving.initiator,
            soort_betrokkene=['Aanvrager'],
            zaaktype__catalogus=self.catalogus,
        )
        rol_type_list_url = reverse('roltype-list')

        response = self.client.get(rol_type_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # TODO: when pagination gets re-added
        # self.assertTrue('results' in data)
        # self.assertEqual(len(data['results']), 1)
        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        rol_type = RolTypeFactory.create(
            omschrijving='Vergunningaanvrager',
            omschrijving_generiek=RolOmschrijving.initiator,
            soort_betrokkene=['Aanvrager'],
            zaaktype__catalogus=self.catalogus,
        )
        zaaktype = rol_type.zaaktype
        rol_type_detail_url = reverse('roltype-detail', kwargs={
            'uuid': rol_type.uuid,
        })
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })

        response = self.client.get(rol_type_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            'url': f'http://testserver{rol_type_detail_url}',
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

    def test_create_roltype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        rol_type_list_url = reverse('roltype-list')
        data = {
            'zaaktype': f'http://testserver{zaaktype_url}',
            'omschrijving': 'Vergunningaanvrager',
            'omschrijvingGeneriek': RolOmschrijving.initiator,
            'mogelijkeBetrokkenen': [],
        }

        response = self.client.post(rol_type_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        roltype = RolType.objects.get()
        self.assertEqual(roltype.omschrijving, 'Vergunningaanvrager')

    def test_delete_roltype(self):
        roltype = RolTypeFactory.create()
        roltype_url = reverse('roltype-detail', kwargs={'uuid': roltype.uuid})

        response = self.client.delete(roltype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RolType.objects.filter(id=roltype.id))

    def test_delete_roltype_fail_not_draft_zaaktype(self):
        roltype = RolTypeFactory.create(zaaktype__draft=False)
        roltype_url = reverse('roltype-detail', kwargs={'uuid': roltype.uuid})

        response = self.client.delete(roltype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-draft object is forbidden')


class FilterValidationTests(APITestCase):

    def test_invalid_filters(self):
        url = reverse('roltype-list')

        invalid_filters = {
            'omschrijvingGeneriek': 'invalid-option',  # bestaat niet
            'foo': 'bar',  # unsupported param
        }

        for key, value in invalid_filters.items():
            with self.subTest(query_param=key, value=value):
                response = self.client.get(url, {key: value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
