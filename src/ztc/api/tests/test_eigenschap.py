from datetime import date
from unittest import skip

from rest_framework import status
from vng_api_common.tests import get_operation_url, get_validation_errors, reverse

from ztc.api.validators import ZaakTypeConceptValidator
from ztc.datamodel.models import Eigenschap, EigenschapSpecificatie
from ztc.datamodel.tests.factories import (
    EigenschapFactory,
    EigenschapReferentieFactory,
    EigenschapSpecificatieFactory,
    ZaakTypeFactory,
)
from ztc.datamodel.tests.factories.statustype import StatusTypeFactory

from ..scopes import SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE
from .base import APITestCase


class EigenschapAPITests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_READ]

    def test_get_list_default_definitief(self):
        eigenschap1 = EigenschapFactory.create(zaaktype__concept=True)
        eigenschap2 = EigenschapFactory.create(zaaktype__concept=False)
        eigenschap_list_url = reverse("eigenschap-list")
        eigenschap2_url = reverse(
            "eigenschap-detail", kwargs={"uuid": eigenschap2.uuid}
        )

        response = self.client.get(eigenschap_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{eigenschap2_url}")

    def test_get_detail(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        statustype = StatusTypeFactory(zaaktype=zaaktype)

        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        statustype_url = reverse("statustype-detail", kwargs={"uuid": statustype.uuid})

        specificatie = EigenschapSpecificatieFactory.create(
            kardinaliteit="1", lengte="1", groep="groep"
        )
        eigenschap = EigenschapFactory.create(
            eigenschapnaam="Beoogd product",
            zaaktype=zaaktype,
            statustype=statustype,
            specificatie_van_eigenschap=specificatie,
            datum_begin_geldigheid=date(2021, 1, 1),
            datum_einde_geldigheid=date(2021, 2, 1),
        )
        eigenschap_detail_url = reverse(
            "eigenschap-detail", kwargs={"uuid": eigenschap.uuid}
        )

        response = self.api_client.get(eigenschap_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            "url": "http://testserver{}".format(eigenschap_detail_url),
            "naam": "Beoogd product",
            "definitie": "",
            "specificatie": {
                "formaat": "",
                "groep": "groep",
                "kardinaliteit": "1",
                "lengte": "1",
                "waardenverzameling": [],
            },
            "toelichting": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "statustype": "http://testserver{}".format(statustype_url),
            "beginGeldigheid": "2021-01-01",
            "eindeGeldigheid": "2021-02-01",
            "beginObject": None,
            "eindeObject": None,
            "zaaktypeIdentificatie": zaaktype.identificatie,
        }
        self.assertEqual(expected, response.json())

    @skip("eigenschap.referentie is not implemented")
    def test_get_detail_reference(self):
        referentie = EigenschapReferentieFactory.create(
            x_path_element="x_path_element", namespace="namespace"
        )
        eigenschap = EigenschapFactory.create(
            eigenschapnaam="Aard product", referentie_naar_eigenschap=referentie
        )
        eigenschap_detail_url = reverse(
            "eigenschap-detail", kwargs={"uuid": eigenschap.uuid}
        )

        response = self.api_client.get(eigenschap_detail_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIsNone(data["specificatie"])
        self.assertEqual(
            data["referentie"],
            {
                "pathElement": "x_path_element",
                "informatiemodel": None,
                "namespace": "namespace",
                "entiteittype": "",
                "schemalocatie": "",
                "objecttype": None,
            },
        )

    def test_create_eigenschap(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        eigenschap_list_url = reverse("eigenschap-list")
        data = {
            "naam": "Beoogd product",
            "definitie": "test",
            "toelichting": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "specificatie": {
                "groep": "test",
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": [],
            },
        }

        response = self.client.post(eigenschap_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        eigenschap = Eigenschap.objects.get()

        self.assertEqual(eigenschap.eigenschapnaam, "Beoogd product")
        self.assertEqual(eigenschap.zaaktype, zaaktype)

        specificatie = eigenschap.specificatie_van_eigenschap
        self.assertEqual(specificatie.groep, "test")
        self.assertEqual(specificatie.formaat, "tekst")
        self.assertEqual(specificatie.lengte, "5")
        self.assertEqual(specificatie.kardinaliteit, "1")
        self.assertEqual(specificatie.waardenverzameling, [])

    def test_create_eigenschap_specificatie_required(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)

        data = {
            "naam": "aangepast",
            "definitie": "test",
            "toelichting": "",
            "zaaktype": zaaktype_url,
        }

        response = self.client.post(reverse(Eigenschap), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "specificatie")
        self.assertEqual(error["code"], "required")

    def test_create_eigenschap_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        eigenschap_list_url = reverse("eigenschap-list")
        data = {
            "naam": "Beoogd product",
            "definitie": "test",
            "toelichting": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "specificatie": {
                "groep": "test",
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": [],
            },
        }

        response = self.client.post(eigenschap_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_delete_eigenschap(self):
        eigenschap = EigenschapFactory.create()
        eigenschap_url = reverse("eigenschap-detail", kwargs={"uuid": eigenschap.uuid})

        response = self.client.delete(eigenschap_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Eigenschap.objects.filter(id=eigenschap.id))

    def test_delete_eigenschap_fail_not_concept_zaaktype(self):
        eigenschap = EigenschapFactory.create(zaaktype__concept=False)
        informatieobjecttypee_url = reverse(
            "eigenschap-detail", kwargs={"uuid": eigenschap.uuid}
        )

        response = self.client.delete(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-zaaktype")

    def test_update_eigenschap(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)
        specificatie = EigenschapSpecificatieFactory.create()
        eigenschap = EigenschapFactory.create(specificatie_van_eigenschap=specificatie)
        eigenschap_url = reverse(eigenschap)

        data = {
            "naam": "aangepast",
            "definitie": "test",
            "toelichting": "",
            "zaaktype": zaaktype_url,
            "specificatie": {
                "groep": "test",
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": [],
            },
        }

        response = self.client.put(eigenschap_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["naam"], "aangepast")

        eigenschap.refresh_from_db()
        self.assertEqual(eigenschap.eigenschapnaam, "aangepast")

        specificatie = EigenschapSpecificatie.objects.get()
        self.assertEqual(specificatie, eigenschap.specificatie_van_eigenschap)

        self.assertEqual(specificatie.groep, "test")
        self.assertEqual(specificatie.formaat, "tekst")
        self.assertEqual(specificatie.lengte, "5")
        self.assertEqual(specificatie.kardinaliteit, "1")
        self.assertEqual(specificatie.waardenverzameling, [])

    def test_update_eigenschap_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        eigenschap = EigenschapFactory.create(zaaktype=zaaktype)
        eigenschap_url = reverse(eigenschap)

        data = {
            "naam": "aangepast",
            "definitie": "test",
            "toelichting": "",
            "zaaktype": zaaktype_url,
            "specificatie": {
                "groep": "test",
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": [],
            },
        }

        response = self.client.put(eigenschap_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_update_eigenschap_add_relation_to_non_concept_zaaktype_fails(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        eigenschap = EigenschapFactory.create()
        eigenschap_url = reverse(eigenschap)

        data = {
            "naam": "aangepast",
            "definitie": "test",
            "toelichting": "",
            "zaaktype": zaaktype_url,
            "specificatie": {
                "groep": "test",
                "formaat": "tekst",
                "lengte": "5",
                "kardinaliteit": "1",
                "waardenverzameling": [],
            },
        }

        response = self.client.put(eigenschap_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_partial_update_eigenschap(self):
        eigenschap = EigenschapFactory.create()
        eigenschap_url = reverse(eigenschap)

        response = self.client.patch(eigenschap_url, {"naam": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["naam"], "aangepast")

        eigenschap.refresh_from_db()
        self.assertEqual(eigenschap.eigenschapnaam, "aangepast")

    def test_partial_update_eigenschap_specificatie(self):
        zaaktype = ZaakTypeFactory.create()
        reverse(zaaktype)
        specificatie = EigenschapSpecificatieFactory.create()
        eigenschap = EigenschapFactory.create()
        eigenschap_url = reverse(eigenschap)

        data = {
            "naam": "aangepast",
            "specificatie": {
                "groep": "test",
            },
        }

        response = self.client.patch(eigenschap_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["naam"], "aangepast")

        eigenschap.refresh_from_db()
        self.assertEqual(eigenschap.eigenschapnaam, "aangepast")

        specificatie = eigenschap.specificatie_van_eigenschap
        self.assertEqual(specificatie.groep, "test")

    def test_partial_update_eigenschap_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        eigenschap = EigenschapFactory.create(zaaktype=zaaktype)
        eigenschap_url = reverse(eigenschap)

        response = self.client.patch(eigenschap_url, {"naam": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_partial_update_eigenschap_add_relation_to_non_concept_zaaktype_fails(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        eigenschap = EigenschapFactory.create()
        eigenschap_url = reverse(eigenschap)

        response = self.client.patch(eigenschap_url, {"zaaktype": zaaktype_url})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)


class EigenschapFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_eigenschap_status_alles(self):
        EigenschapFactory.create(zaaktype__concept=True)
        EigenschapFactory.create(zaaktype__concept=False)
        eigenschap_list_url = reverse("eigenschap-list")

        response = self.client.get(eigenschap_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_eigenschap_status_concept(self):
        eigenschap1 = EigenschapFactory.create(zaaktype__concept=True)
        eigenschap2 = EigenschapFactory.create(zaaktype__concept=False)
        eigenschap_list_url = reverse("eigenschap-list")
        eigenschap1_url = reverse(
            "eigenschap-detail", kwargs={"uuid": eigenschap1.uuid}
        )

        response = self.client.get(eigenschap_list_url, {"status": "concept"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{eigenschap1_url}")

    def test_filter_eigenschap_status_definitief(self):
        eigenschap1 = EigenschapFactory.create(zaaktype__concept=True)
        eigenschap2 = EigenschapFactory.create(zaaktype__concept=False)
        eigenschap_list_url = reverse("eigenschap-list")
        eigenschap2_url = reverse(
            "eigenschap-detail", kwargs={"uuid": eigenschap2.uuid}
        )

        response = self.client.get(eigenschap_list_url, {"status": "definitief"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{eigenschap2_url}")

    def test_filter_zaaktype_identificatie(self):
        eigenschap1 = EigenschapFactory.create(
            zaaktype__concept=False,
        )
        eigenschap2 = EigenschapFactory.create(
            zaaktype__concept=False,
        )

        list_url = reverse("eigenschap-list")
        response = self.client.get(
            list_url, {"zaaktypeIdentificatie": eigenschap1.zaaktype.identificatie}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(eigenschap1)}")

    def test_filter_zaaktype_datum_geldigheid_get_latest_version(self):
        eigenschap1 = EigenschapFactory.create(
            zaaktype__concept=False,
            zaaktype__identificatie="123",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        eigenschap2 = EigenschapFactory.create(
            zaaktype__concept=False,
            zaaktype__identificatie="123",
            datum_begin_geldigheid="2020-02-02",
            datum_einde_geldigheid="2020-03-01",
        )
        eigenschap3 = EigenschapFactory.create(
            zaaktype__concept=False,
            zaaktype__identificatie="123",
            datum_begin_geldigheid="2020-03-02",
        )
        list_url = reverse("eigenschap-list")
        response = self.client.get(
            list_url,
            {
                "datumGeldigheid": "2020-03-05",
                "zaaktypeIdentificatie": "123",
            },
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["beginGeldigheid"], eigenschap3.datum_begin_geldigheid)

    def test_filter_zaaktype_datum_geldigheid_get_older_version(self):
        eigenschap1 = EigenschapFactory.create(
            zaaktype__concept=False,
            zaaktype__identificatie="123",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        eigenschap2 = EigenschapFactory.create(
            zaaktype__concept=False,
            zaaktype__identificatie="123",
            datum_begin_geldigheid="2020-02-02",
            datum_einde_geldigheid="2020-03-01",
        )
        eigenschap3 = EigenschapFactory.create(
            zaaktype__concept=False,
            zaaktype__identificatie="123",
            datum_begin_geldigheid="2020-03-02",
        )
        list_url = reverse("eigenschap-list")
        response = self.client.get(
            list_url,
            {
                "datumGeldigheid": "2020-02-15",
                "zaaktypeIdentificatie": "123",
            },
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["beginGeldigheid"], eigenschap2.datum_begin_geldigheid)


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        EigenschapFactory.create_batch(2)
        eigenschap_list_url = get_operation_url("eigenschap_list")

        response = self.client.get(eigenschap_list_url, {"someparam": "somevalue"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


class EigenschapPaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        EigenschapFactory.create_batch(2, zaaktype__concept=False)
        eigenschap_list_url = reverse("eigenschap-list")

        response = self.client.get(eigenschap_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        EigenschapFactory.create_batch(2, zaaktype__concept=False)
        eigenschap_list_url = reverse("eigenschap-list")

        response = self.client.get(eigenschap_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
