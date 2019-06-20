from rest_framework import status
from ztc.datamodel.models import Catalogus

from .base import APITestCase


class CatalogusAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `Catalog` objects."""
        response = self.client.get(self.catalogus_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `Catalog` object."""
        response = self.client.get(self.catalogus_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'domein': self.catalogus.domein,
            'url': 'http://testserver{}'.format(self.catalogus_detail_url),
            'contactpersoonBeheerTelefoonnummer': '0612345678',
            'rsin': self.catalogus.rsin,
            'contactpersoonBeheerNaam': self.catalogus.contactpersoon_beheer_naam,
            'contactpersoonBeheerEmailadres': self.catalogus.contactpersoon_beheer_emailadres,
            'informatieobjecttypen': [],
            'zaaktypen': [],
            'besluittypen': [],
        }
        self.assertEqual(response.json(), expected)

    def test_create_catalogus(self):
        data = {
            'domein': 'TEST',
            'contactpersoonBeheerTelefoonnummer': '0612345679',
            'rsin': '100000009',
            'contactpersoonBeheerNaam': 'test',
            'contactpersoonBeheerEmailadres': 'test@test.com',
        }

        response = self.client.post(self.catalogus_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        catalog = Catalogus.objects.get(domein='TEST')

        self.assertEqual(catalog.rsin, '100000009')
