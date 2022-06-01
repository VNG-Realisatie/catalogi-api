from datetime import date

from rest_framework import status
from vng_api_common.tests import get_operation_url, get_validation_errors, reverse

from ztc.api.validators import ZaakTypeConceptValidator
from ztc.datamodel.models import StatusType
from ztc.datamodel.tests.factories import StatusTypeFactory, ZaakTypeFactory
from ztc.datamodel.tests.factories.eigenschap import EigenschapFactory
from ztc.datamodel.tests.factories.statustype import CheckListItemFactory

from ..scopes import SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE
from .base import APITestCase


class StatusTypeAPITests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_READ]

    def test_get_list_default_definitief(self):
        statustype1 = StatusTypeFactory.create(zaaktype__concept=True)
        statustype2 = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse("statustype-list")
        statustype2_url = reverse(
            "statustype-detail", kwargs={"uuid": statustype2.uuid}
        )

        response = self.client.get(statustype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{statustype2_url}")

    def test_get_detail(self):
        zaaktype = ZaakTypeFactory(catalogus=self.catalogus)
        eigenschap = EigenschapFactory(zaaktype=zaaktype)
        statustype = StatusTypeFactory(
            statustype_omschrijving="Besluit genomen",
            datum_begin_geldigheid=date(2021, 1, 1),
            datum_einde_geldigheid=date(2021, 2, 1),
            zaaktype=zaaktype,
            eigenschappen=[eigenschap],
            doorlooptijd_status="P30D",
            toelichting="Toelichting X",
            checklistitems=[
                CheckListItemFactory(
                    itemnaam="Item 1",
                    toelichting="Controleren op de itemnaam",
                    verplicht=True,
                    vraagstelling="Is item 1, item nummer een?",
                )
            ],
        )

        statustype_detail_url = reverse(
            "statustype-detail", kwargs={"uuid": statustype.uuid}
        )
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        eigenschap_url = reverse("eigenschap-detail", kwargs={"uuid": eigenschap.uuid})

        response = self.api_client.get(statustype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            "url": "http://testserver{}".format(statustype_detail_url),
            "omschrijving": "Besluit genomen",
            "omschrijvingGeneriek": "",
            "statustekst": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "volgnummer": statustype.statustypevolgnummer,
            "isEindstatus": True,
            "informeren": False,
            "doorlooptijd": "P30D",
            "toelichting": "Toelichting X",
            "checklistitemStatustype": [
                {
                    "itemnaam": "Item 1",
                    "toelichting": "Controleren op de itemnaam",
                    "verplicht": True,
                    "vraagstelling": "Is item 1, item nummer een?",
                }
            ],
            "eigenschappen": [f"http://testserver{eigenschap_url}"],
            "beginGeldigheid": "2021-01-01",
            "eindeGeldigheid": "2021-02-01",
        }

        self.assertEqual(expected, response.json())

    def test_create_statustype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        statustype_list_url = reverse("statustype-list")
        data = {
            "omschrijving": "Besluit genomen",
            "omschrijvingGeneriek": "",
            "statustekst": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "volgnummer": 2,
        }
        response = self.client.post(statustype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        statustype = StatusType.objects.get()

        self.assertEqual(statustype.statustype_omschrijving, "Besluit genomen")
        self.assertEqual(statustype.zaaktype, zaaktype)

    def test_create_statustype_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        statustype_list_url = reverse("statustype-list")
        data = {
            "omschrijving": "Besluit genomen",
            "omschrijvingGeneriek": "",
            "statustekst": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "volgnummer": 2,
        }
        response = self.client.post(statustype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_delete_statustype(self):
        statustype = StatusTypeFactory.create()
        statustype_url = reverse("statustype-detail", kwargs={"uuid": statustype.uuid})

        response = self.client.delete(statustype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(StatusType.objects.filter(id=statustype.id))

    def test_delete_statustype_fail_not_concept_zaaktype(self):
        statustype = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_url = reverse("statustype-detail", kwargs={"uuid": statustype.uuid})

        response = self.client.delete(statustype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_update_statustype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)
        statustype = StatusTypeFactory.create(zaaktype=zaaktype)
        statustype_url = reverse(statustype)

        data = {
            "omschrijving": "aangepast",
            "omschrijvingGeneriek": "",
            "statustekst": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "volgnummer": 2,
        }

        response = self.client.put(statustype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "aangepast")

        statustype.refresh_from_db()
        self.assertEqual(statustype.statustype_omschrijving, "aangepast")

    def test_update_statustype_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        statustype = StatusTypeFactory.create(zaaktype=zaaktype)
        statustype_url = reverse(statustype)

        data = {
            "omschrijving": "aangepast",
            "omschrijvingGeneriek": "",
            "statustekst": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "volgnummer": 2,
        }

        response = self.client.put(statustype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_update_statustype_add_relation_to_non_concept_zaaktype_fails(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        statustype = StatusTypeFactory.create()
        statustype_url = reverse(statustype)

        data = {
            "omschrijving": "aangepast",
            "omschrijvingGeneriek": "",
            "statustekst": "",
            "zaaktype": "http://testserver{}".format(zaaktype_url),
            "volgnummer": 2,
        }

        response = self.client.put(statustype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_partial_update_statustype(self):
        zaaktype = ZaakTypeFactory.create()
        reverse(zaaktype)
        statustype = StatusTypeFactory.create(zaaktype=zaaktype)
        statustype_url = reverse(statustype)

        response = self.client.patch(statustype_url, {"omschrijving": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "aangepast")

        statustype.refresh_from_db()
        self.assertEqual(statustype.statustype_omschrijving, "aangepast")

    def test_partial_update_statustype_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        reverse(zaaktype)
        statustype = StatusTypeFactory.create(zaaktype=zaaktype)
        statustype_url = reverse(statustype)

        response = self.client.patch(statustype_url, {"omschrijving": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)

    def test_partial_update_statustype_add_relation_to_non_concept_zaaktype_fails(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        statustype = StatusTypeFactory.create()
        statustype_url = reverse(statustype)

        response = self.client.patch(statustype_url, {"zaaktype": zaaktype_url})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ZaakTypeConceptValidator.code)


class StatusTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_statustype_status_alles(self):
        StatusTypeFactory.create(zaaktype__concept=True)
        StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse("statustype-list")

        response = self.client.get(statustype_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_statustype_status_concept(self):
        statustype1 = StatusTypeFactory.create(zaaktype__concept=True)
        statustype2 = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse("statustype-list")
        statustype1_url = reverse(
            "statustype-detail", kwargs={"uuid": statustype1.uuid}
        )

        response = self.client.get(statustype_list_url, {"status": "concept"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{statustype1_url}")

    def test_filter_statustype_status_definitief(self):
        statustype1 = StatusTypeFactory.create(zaaktype__concept=True)
        statustype2 = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse("statustype-list")
        statustype2_url = reverse(
            "statustype-detail", kwargs={"uuid": statustype2.uuid}
        )

        response = self.client.get(statustype_list_url, {"status": "definitief"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{statustype2_url}")

    def test_filter_zaaktype_identificatie(self):
        statustype1 = StatusTypeFactory.create(
            zaaktype__concept=False,
        )
        statustype2 = StatusTypeFactory.create(
            zaaktype__concept=False,
        )

        list_url = reverse("statustype-list")
        response = self.client.get(
            list_url, {"zaaktypeIdentificatie": statustype1.zaaktype_identificatie}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["zaaktypeIdentificatie"], statustype1.zaaktype_identificatie
        )

    def test_filter_zaaktype_datum_geldigheid_get_latest_version(self):
        statustype1 = StatusTypeFactory.create(
            zaaktype__concept=False,
            zaaktype_identificatie="123",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        statustype2 = StatusTypeFactory.create(
            zaaktype__concept=False,
            zaaktype_identificatie="123",
            datum_begin_geldigheid="2020-02-02",
            datum_einde_geldigheid="2020-03-01",
        )
        statustype3 = StatusTypeFactory.create(
            zaaktype__concept=False,
            zaaktype_identificatie="123",
            datum_begin_geldigheid="2020-03-02",
        )
        list_url = reverse("statustype-list")
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
        self.assertEqual(data[0]["beginGeldigheid"], statustype3.datum_begin_geldigheid)

    def test_filter_zaaktype_datum_geldigheid_get_older_version(self):
        statustype1 = StatusTypeFactory.create(
            zaaktype__concept=False,
            zaaktype_identificatie="123",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        statustype2 = StatusTypeFactory.create(
            zaaktype__concept=False,
            zaaktype_identificatie="123",
            datum_begin_geldigheid="2020-02-02",
            datum_einde_geldigheid="2020-03-01",
        )
        statustype3 = StatusTypeFactory.create(
            zaaktype__concept=False,
            zaaktype_identificatie="123",
            datum_begin_geldigheid="2020-03-02",
        )
        list_url = reverse("statustype-list")
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
        self.assertEqual(data[0]["beginGeldigheid"], statustype2.datum_begin_geldigheid)


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        StatusTypeFactory.create_batch(2)
        statustype_list_url = get_operation_url("statustype_list")

        response = self.client.get(statustype_list_url, {"someparam": "somevalue"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


class StatusTypePaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        StatusTypeFactory.create_batch(2, zaaktype__concept=False)
        statustype_list_url = reverse("statustype-list")

        response = self.client.get(statustype_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        StatusTypeFactory.create_batch(2, zaaktype__concept=False)
        statustype_list_url = reverse("statustype-list")

        response = self.client.get(statustype_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
