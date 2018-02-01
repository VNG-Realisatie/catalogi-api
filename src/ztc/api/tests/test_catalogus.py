from ztc.api.tests.base import APITestCase


class CatalogusAPITests(APITestCase):
    def test_get_list(self):
        """Retrieve a list of `Catalog` objects."""
        response = self.api_client.get(self.catalogus_list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_detail(self):
        """Retrieve the details of a single `Catalog` object."""
        response = self.api_client.get(self.catalogus_detail_url)
        self.assertEqual(response.status_code, 200)
