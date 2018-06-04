from ztc.api.tests.base import APITestCase


class CatalogusAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `Catalog` objects."""
        response = self.api_client.get(self.catalogus_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

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
            # 'bestaatuitInformatieobjecttype': [],
            'bestaatuitZaaktype': [],
            # 'bestaatuitBesluittype': []
        }
        self.assertEqual(response.json(), expected)

    def test_bestaatuit_informatieobjecttype(self):
        pass

    def test_bestaatuit_zaaktype(self):
        pass

    def test_bestaatuit_besluittype(self):
        pass
