import unittest

from .base import APITestCase


class CatalogusAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `Catalog` objects."""
        response = self.api_client.get(self.catalogus_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `Catalog` object."""
        response = self.api_client.get(self.catalogus_detail_url)
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

    @unittest.expectedFailure
    def test_bestaatuit_informatieobjecttype(self):
        raise NotImplementedError

    @unittest.expectedFailure
    def test_bestaatuit_zaaktype(self):
        raise NotImplementedError

    @unittest.expectedFailure
    def test_bestaatuit_besluittype(self):
        raise NotImplementedError
