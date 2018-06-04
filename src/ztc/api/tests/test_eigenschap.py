from unittest import skip

from django.urls import reverse

from ztc.datamodel.tests.factories import (
    EigenschapFactory, EigenschapReferentieFactory,
    EigenschapSpecificatieFactory, ZaakTypeFactory
)

from .base import APITestCase


@skip("Not MVP yet")
class EigenschapAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.zaaktype = ZaakTypeFactory.create(maakt_deel_uit_van=self.catalogus)

        specificatie = EigenschapSpecificatieFactory.create(
            kardinaliteit='1',
            lengte='1',
            groep='groep',
        )
        self.eigenschap_one = EigenschapFactory.create(
            eigenschapnaam='Beoogd product',
            is_van=self.zaaktype,
            specificatie_van_eigenschap=specificatie
        )

        referentie = EigenschapReferentieFactory.create(
            x_path_element='x_path_element',
            namespace='namespace',
        )
        self.eigenschap_two = EigenschapFactory.create(
            eigenschapnaam='Aard product',
            is_van=self.zaaktype,
            referentie_naar_eigenschap=referentie
        )

        self.eigenschap_list_url = reverse('api:eigenschap-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.eigenschap_one_detail_url = reverse('api:eigenschap-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.eigenschap_one.pk
        })
        self.eigenschap_two_detail_url = reverse('api:eigenschap-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.eigenschap_two.pk
        })

    def test_get_list(self):
        response = self.api_client.get(self.eigenschap_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 2)

    def test_get_detail(self):
        response = self.api_client.get(self.eigenschap_one_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'definitie': '',
            'einddatumObject': None,
            'ingangsdatumObject': '2018-01-01',
            'isVan': 'http://testserver{}'.format(
                reverse('api:zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk])
            ),
            'naam': 'Beoogd product',
            'referentie': None,
            'specificatie': {
                'formaat': '',
                'groep': 'groep',
                'kardinaliteit': '1',
                'lengte': '1',
                'waardeverzameling': []
            },
            'toelichting': None,
            'url': 'http://testserver{}'.format(self.eigenschap_one_detail_url)
        }
        self.assertEqual(expected, response.json())

    def test_get_detail_reference(self):
        response = self.api_client.get(self.eigenschap_two_detail_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsNone(data['specificatie'])
        self.assertEqual(
            data['referentie'],
            {
                'pathElement': 'x_path_element',
                'informatiemodel': None,
                'namespace': 'namespace',
                'entiteittype': '',
                'schemalocatie': '',
                'objecttype': None
            },
        )
