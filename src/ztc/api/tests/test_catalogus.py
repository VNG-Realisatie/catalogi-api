from datetime import date

from rest_framework import status
from vng_api_common.tests import get_operation_url, get_validation_errors, reverse

from ztc.datamodel.models import Catalogus
from ztc.datamodel.tests.factories import CatalogusFactory

from .base import APITestCase


class CatalogusAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `Catalog` objects."""
        response = self.client.get(self.catalogus_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `Catalog` object."""
        response = self.client.get(self.catalogus_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            "domein": self.catalogus.domein,
            "url": "http://testserver{}".format(self.catalogus_detail_url),
            "contactpersoonBeheerTelefoonnummer": "0612345678",
            "rsin": self.catalogus.rsin,
            "contactpersoonBeheerNaam": self.catalogus.contactpersoon_beheer_naam,
            "contactpersoonBeheerEmailadres": self.catalogus.contactpersoon_beheer_emailadres,
            "informatieobjecttypen": [],
            "zaaktypen": [],
            "besluittypen": [],
            "naam": self.catalogus.naam,
            "versie": self.catalogus.versie,
            "begindatumVersie": str(self.catalogus.datum_begin_versie),
        }
        self.assertEqual(response.json(), expected)

    def test_create_catalogus(self):
        data = {
            "domein": "TEST",
            "contactpersoonBeheerTelefoonnummer": "0612345679",
            "rsin": "100000009",
            "contactpersoonBeheerNaam": "test",
            "contactpersoonBeheerEmailadres": "test@test.com",
        }

        response = self.client.post(self.catalogus_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        catalog = Catalogus.objects.get(domein="TEST")

        self.assertEqual(catalog.rsin, "100000009")

    def test_create_catalogus_new_fields(self):
        data = {
            "domein": "TEST",
            "contactpersoonBeheerTelefoonnummer": "0612345679",
            "rsin": "100000009",
            "contactpersoonBeheerNaam": "test",
            "contactpersoonBeheerEmailadres": "test@test.com",
            "naam": "Category X",
            "versie": "1",
            "begindatumVersie": "2019-01-01",
        }

        response = self.client.post(self.catalogus_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        catalog = Catalogus.objects.get(domein="TEST")

        self.assertEqual(catalog.naam, "Category X")
        self.assertEqual(catalog.versie, "1")
        self.assertEqual(catalog.datum_begin_versie, date(2019, 1, 1))

    def test_create_catalogus_rsin_only_digits(self):
        data = {
            "domein": "TEST",
            "contactpersoonBeheerTelefoonnummer": "0612345679",
            "rsin": "blabla",
            "contactpersoonBeheerNaam": "test",
            "contactpersoonBeheerEmailadres": "test@test.com",
        }

        response = self.client.post(self.catalogus_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "rsin")
        self.assertEqual(error["code"], "only-digits")

    def test_create_catalogus_rsin_invalid_length(self):
        data = {
            "domein": "TEST",
            "contactpersoonBeheerTelefoonnummer": "0612345679",
            "rsin": "0000",
            "contactpersoonBeheerNaam": "test",
            "contactpersoonBeheerEmailadres": "test@test.com",
        }

        response = self.client.post(self.catalogus_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "rsin")
        self.assertEqual(error["code"], "invalid-length")


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        CatalogusFactory.create_batch(2)
        catalogus_list_url = get_operation_url("catalogus_list")

        response = self.client.get(catalogus_list_url, {"someparam": "somevalue"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


class CatalogusFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_domein_exact(self):
        catalogus1 = CatalogusFactory.create(domein="ABC")
        catalogus2 = CatalogusFactory.create(domein="DEF")

        response = self.client.get(self.catalogus_list_url, {"domein": "ABC"})

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(catalogus1)}")

    def test_filter_domein_in(self):
        catalogus1 = CatalogusFactory.create(domein="ABC")
        catalogus2 = CatalogusFactory.create(domein="DEF")

        response = self.client.get(self.catalogus_list_url, {"domein__in": "ABC,AAA"})

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(catalogus1)}")

    def test_filter_rsin_exact(self):
        catalogus1 = CatalogusFactory.create(rsin="100000009")
        catalogus2 = CatalogusFactory.create(rsin="100000020")

        response = self.client.get(self.catalogus_list_url, {"rsin": "100000009"})

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(catalogus1)}")

    def test_filter_rsin_in(self):
        catalogus1 = CatalogusFactory.create(rsin="100000009")
        catalogus2 = CatalogusFactory.create(rsin="100000022")

        response = self.client.get(
            self.catalogus_list_url, {"rsin__in": "100000009,100000010"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(catalogus1)}")


class CatalogusPaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        response = self.client.get(self.catalogus_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 1)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        response = self.client.get(self.catalogus_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 1)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
