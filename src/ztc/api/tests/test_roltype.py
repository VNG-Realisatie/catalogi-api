from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time

from ztc.datamodel.tests.base_tests import HaaglandenMixin

from .base import ClientAPITestMixin


@freeze_time('2018-02-07')  # datum_begin_geldigheid will be 'today': 'V20180207'
class RolTypeAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.list_url = reverse('api:roltype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.rol_type_vergunnings_aanvrager_detail_url = reverse('api:roltype-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.rol_type_vergunnings_aanvrager.pk,
        })

    def test_get_list(self):
        # let the magZetten list empty in this test
        self.rol_type_vergunnings_aanvrager.mag_zetten.all().delete()

        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        results = json_response.pop('results')
        self.assertEqual(len(results), 7)

        self.assertEqual(results[0], {
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/roltypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.rol_type_vergunnings_aanvrager.pk),
            'ingangsdatumObject': 'V20180207',
            'einddatumObject': None,
            'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk),
            'omschrijving': 'Vergunningaanvrager',
            'omschrijvingGeneriek': 'Initiator',
            'soortBetrokkene': ['Aanvrager'],
            'magZetten': [],
        })

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/roltypen/'.format(
                        self.catalogus.pk, self.zaaktype.pk)
                }
            },
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail(self):
        response = self.api_client.get(self.rol_type_vergunnings_aanvrager_detail_url)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        magZetten = response_json.pop('magZetten')
        self.assertEqual(len(magZetten), 4)
        for statustype in magZetten:
            self.assertTrue(statustype.startswith('http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/statustypen/'.format(
                self.catalogus.pk, self.zaaktype.pk)))

        expected = {
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/roltypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.rol_type_vergunnings_aanvrager.pk),
            'ingangsdatumObject': 'V20180207',
            'einddatumObject': None,
            'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk),
            'omschrijving': 'Vergunningaanvrager',
            'omschrijvingGeneriek': 'Initiator',
            'soortBetrokkene': ['Aanvrager'],
        }
        self.assertEqual(expected, response_json)
