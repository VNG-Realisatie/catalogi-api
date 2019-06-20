from unittest import skip

from rest_framework import status
from ztc.datamodel.tests.factories import (
    EigenschapFactory, EigenschapReferentieFactory,
    EigenschapSpecificatieFactory, ZaakTypeFactory
)
from ztc.datamodel.models import Eigenschap

from .base import APITestCase
from .utils import reverse


class EigenschapAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        EigenschapFactory.create_batch(2)
        eigenschap_list_url = reverse('eigenschap-list')

        response = self.api_client.get(eigenschap_list_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 2)

    def test_get_detail(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_url = reverse('zaaktype-detail', kwargs={'uuid': zaaktype.uuid})
        specificatie = EigenschapSpecificatieFactory.create(
            kardinaliteit='1',
            lengte='1',
            groep='groep',
        )
        eigenschap = EigenschapFactory.create(
            eigenschapnaam='Beoogd product',
            zaaktype=zaaktype,
            specificatie_van_eigenschap=specificatie
        )
        eigenschap_detail_url = reverse('eigenschap-detail', kwargs={
            'uuid': eigenschap.uuid
        })

        response = self.api_client.get(eigenschap_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver{}'.format(eigenschap_detail_url),
            'naam': 'Beoogd product',
            'definitie': '',
            'specificatie': {
                'formaat': '',
                'groep': 'groep',
                'kardinaliteit': '1',
                'lengte': '1',
                'waardenverzameling': []
            },
            'toelichting': '',
            'zaaktype': 'http://testserver{}'.format(zaaktype_url),
        }
        self.assertEqual(expected, response.json())

    @skip("eigenschap.referentie is not implemented")
    def test_get_detail_reference(self):
        referentie = EigenschapReferentieFactory.create(
            x_path_element='x_path_element',
            namespace='namespace',
        )
        eigenschap = EigenschapFactory.create(
            eigenschapnaam='Aard product',
            referentie_naar_eigenschap=referentie
        )
        eigenschap_detail_url = reverse('eigenschap-detail', kwargs={
            'uuid': eigenschap.uuid
        })

        response = self.api_client.get(eigenschap_detail_url)

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

    def test_create_eigenschap(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_url = reverse('zaaktype-detail', kwargs={'uuid': zaaktype.uuid})
        eigenschap_list_url = reverse('eigenschap-list')
        data = {
            'naam': 'Beoogd product',
            'definitie': 'test',
            'toelichting': '',
            'zaaktype': 'http://testserver{}'.format(zaaktype_url),
        }

        response = self.client.post(eigenschap_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        eigenschap = Eigenschap.objects.get()

        self.assertEqual(eigenschap.eigenschapnaam, 'Beoogd product')
        self.assertEqual(eigenschap.zaaktype, zaaktype)
