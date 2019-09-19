from rest_framework import status
from vng_api_common.constants import RolOmschrijving
from vng_api_common.tests import get_operation_url, get_validation_errors, reverse

from ...datamodel.models import RolType
from ...datamodel.tests.factories import RolTypeFactory, ZaakTypeFactory
from .base import APITestCase


class RolTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list_default_definitief(self):
        roltype1 = RolTypeFactory.create(zaaktype__concept=True)
        roltype2 = RolTypeFactory.create(zaaktype__concept=False)
        roltype_list_url = reverse("roltype-list")
        roltype2_url = reverse("roltype-detail", kwargs={"uuid": roltype2.uuid})

        response = self.client.get(roltype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{roltype2_url}")

    def test_get_detail(self):
        rol_type = RolTypeFactory.create(
            omschrijving="Vergunningaanvrager",
            omschrijving_generiek=RolOmschrijving.initiator,
            soort_betrokkene=["Aanvrager"],
            zaaktype__catalogus=self.catalogus,
        )
        zaaktype = rol_type.zaaktype
        rol_type_detail_url = reverse("roltype-detail", kwargs={"uuid": rol_type.uuid})
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})

        response = self.client.get(rol_type_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            "url": f"http://testserver{rol_type_detail_url}",
            # 'ingangsdatumObject': '2018-01-01',
            # 'einddatumObject': None,
            "zaaktype": f"http://testserver{zaaktype_url}",
            "omschrijving": "Vergunningaanvrager",
            "omschrijvingGeneriek": RolOmschrijving.initiator,
        }
        self.assertEqual(expected, response.json())

    def test_mag_zetten(self):
        pass

    def test_create_roltype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        rol_type_list_url = reverse("roltype-list")
        data = {
            "zaaktype": f"http://testserver{zaaktype_url}",
            "omschrijving": "Vergunningaanvrager",
            "omschrijvingGeneriek": RolOmschrijving.initiator,
        }

        response = self.client.post(rol_type_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        roltype = RolType.objects.get()
        self.assertEqual(roltype.omschrijving, "Vergunningaanvrager")
        self.assertEqual(roltype.zaaktype, zaaktype)

    def test_create_roltype_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        rol_type_list_url = reverse("roltype-list")
        data = {
            "zaaktype": f"http://testserver{zaaktype_url}",
            "omschrijving": "Vergunningaanvrager",
            "omschrijvingGeneriek": RolOmschrijving.initiator,
        }

        response = self.client.post(rol_type_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(
            data["detail"],
            "Creating a related object to non-concept object is forbidden",
        )

    def test_delete_roltype(self):
        roltype = RolTypeFactory.create()
        roltype_url = reverse("roltype-detail", kwargs={"uuid": roltype.uuid})

        response = self.client.delete(roltype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RolType.objects.filter(id=roltype.id))

    def test_delete_roltype_fail_not_concept_zaaktype(self):
        roltype = RolTypeFactory.create(zaaktype__concept=False)
        roltype_url = reverse("roltype-detail", kwargs={"uuid": roltype.uuid})

        response = self.client.delete(roltype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data["detail"], "Alleen concepten kunnen worden verwijderd.")


class FilterValidationTests(APITestCase):
    def test_invalid_filters(self):
        url = reverse("roltype-list")

        invalid_filters = {
            "omschrijvingGeneriek": "invalid-option",  # bestaat niet
            "foo": "bar",  # unsupported param
        }

        for key, value in invalid_filters.items():
            with self.subTest(query_param=key, value=value):
                response = self.client.get(url, {key: value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RolTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_roltype_status_alles(self):
        RolTypeFactory.create(zaaktype__concept=True)
        RolTypeFactory.create(zaaktype__concept=False)
        roltype_list_url = reverse("roltype-list")

        response = self.client.get(roltype_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_roltype_status_concept(self):
        roltype1 = RolTypeFactory.create(zaaktype__concept=True)
        roltype2 = RolTypeFactory.create(zaaktype__concept=False)
        roltype_list_url = reverse("roltype-list")
        roltype1_url = reverse("roltype-detail", kwargs={"uuid": roltype1.uuid})

        response = self.client.get(roltype_list_url, {"status": "concept"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{roltype1_url}")

    def test_filter_roltype_status_definitief(self):
        roltype1 = RolTypeFactory.create(zaaktype__concept=True)
        roltype2 = RolTypeFactory.create(zaaktype__concept=False)
        roltype_list_url = reverse("roltype-list")
        roltype2_url = reverse("roltype-detail", kwargs={"uuid": roltype2.uuid})

        response = self.client.get(roltype_list_url, {"status": "definitief"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{roltype2_url}")

    def test_filter_zaaktype(self):
        roltype1 = RolTypeFactory.create(zaaktype__concept=False)
        roltype2 = RolTypeFactory.create(zaaktype__concept=False)
        zaaktype1 = roltype1.zaaktype
        roltype_list_url = reverse("roltype-list")
        roltype1_url = reverse(roltype1)
        zaaktype1_url = reverse(zaaktype1)

        response = self.client.get(roltype_list_url, {"zaaktype": zaaktype1_url})

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{roltype1_url}")


class RolTypePaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        RolTypeFactory.create_batch(2, zaaktype__concept=False)
        roltype_list_url = reverse("roltype-list")

        response = self.client.get(roltype_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        RolTypeFactory.create_batch(2, zaaktype__concept=False)
        roltype_list_url = reverse("roltype-list")

        response = self.client.get(roltype_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
