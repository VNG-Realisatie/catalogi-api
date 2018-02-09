from ztc.api.tests.base import APITestCase


class CatalogusAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `Catalog` objects."""
        response = self.api_client.get(self.catalogus_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/'
                }
            },
            'results': [
                {
                    'contactpersoonBeheerEmailadres': self.catalogus.contactpersoon_beheer_emailadres,
                    'rsin': self.catalogus.rsin,
                    'bestaatuitZaaktype': [],
                    'url': 'http://testserver/api/v1/catalogussen/{}/'.format(self.catalogus.pk),
                    'contactpersoonBeheerNaam': self.catalogus.contactpersoon_beheer_naam,
                    'bestaatuitBesluittype': [],
                    'contactpersoonBeheerTelefoonnummer': '0612345678',
                    'domein': self.catalogus.domein,
                    'bestaatuitInformatieobjecttype': []
                }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail(self):
        """Retrieve the details of a single `Catalog` object."""
        response = self.api_client.get(self.catalogus_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'domein': self.catalogus.domein,
            'url': 'http://testserver/api/v1/catalogussen/{}/'.format(self.catalogus.pk),
            'contactpersoonBeheerTelefoonnummer': '0612345678',
            'rsin': self.catalogus.rsin,
            'contactpersoonBeheerNaam': self.catalogus.contactpersoon_beheer_naam,
            'contactpersoonBeheerEmailadres': self.catalogus.contactpersoon_beheer_emailadres,
            'bestaatuitInformatieobjecttype': [],
            'bestaatuitZaaktype': [],
            'bestaatuitBesluittype': []
        }
        self.assertEqual(response.json(), expected)
