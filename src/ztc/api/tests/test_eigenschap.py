from django.test import TestCase
from django.urls import reverse

from ztc.datamodel.tests.base_tests import HaaglandenMixin
from .base import ClientAPITestMixin


class EigenschapAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.eigenschap_list_url = reverse('api:eigenschap-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })

    def test_get_list(self):
        response = self.api_client.get(self.eigenschap_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links':
                {'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/eigenschappen/'.format(self.catalogus.pk, self.zaaktype.pk)}
                 },
            'results': [
                {
                    'status_type': None,
                    'toelichting': '',
                    'eigenschapnaam': 'Beoogd(e) product(en',
                    'definitie': ''
                }, {
                    'status_type': None,
                    'toelichting': 'Nieuw / Verandering / Ambtshalve wijziging / Ontheffing / Intrekking',
                    'eigenschapnaam': 'Aard product',
                    'definitie': ''
                }
            ]
        }

        self.assertEqual(response.json(), expected)
