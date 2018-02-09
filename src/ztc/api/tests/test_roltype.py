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
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        results = json_response.pop('results')
        self.assertEqual(len(results), 7)

        self.assertEqual(results[0], {
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/roltypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.rol_type_vergunnings_aanvrager.pk),
            'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk),
            'roltypeomschrijving': 'Vergunningaanvrager',
            'soort_betrokkene': ['Aanvrager'],
            'roltypeomschrijving_generiek': 'Initiator'
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

        expected = {
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/roltypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.rol_type_vergunnings_aanvrager.pk),
            'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk),
            'roltypeomschrijving': 'Vergunningaanvrager',
            'soort_betrokkene': ['Aanvrager'],
            'roltypeomschrijving_generiek': 'Initiator'
        }
        self.assertEqual(expected, response.json())
