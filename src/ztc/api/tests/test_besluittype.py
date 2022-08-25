from datetime import date, timedelta

from rest_framework import status
from vng_api_common.tests import (
    JWTAuthMixin,
    get_operation_url,
    get_validation_errors,
    reverse,
)

from ztc.api.validators import (
    ConceptUpdateValidator,
    M2MConceptCreateValidator,
    M2MConceptUpdateValidator,
)
from ztc.datamodel.tests.factories.resultaattype import ResultaatTypeFactory

from ...datamodel.models import BesluitType
from ...datamodel.tests.factories import (
    BesluitTypeFactory,
    CatalogusFactory,
    InformatieObjectTypeFactory,
    ZaakTypeFactory,
)
from ..scopes import (
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from .base import APITestCase


class BesluitTypeAPITests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE]

    def test_get_list_default_definitief(self):
        besluittype1 = BesluitTypeFactory.create(concept=True)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        besluittype_list_url = reverse("besluittype-list")
        besluittype2_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype2.uuid}
        )

        response = self.client.get(besluittype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype2_url}")

    def test_get_detail(self):
        """Retrieve the details of a single `BesluitType` object."""
        zaaktype = ZaakTypeFactory(catalogus=self.catalogus)

        resultaattype = ResultaatTypeFactory(zaaktype=zaaktype)

        besluittype = BesluitTypeFactory(
            catalogus=self.catalogus,
            zaaktypen=[zaaktype],
            resultaattypen=[resultaattype],
            publicatie_indicatie=True,
        )

        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        besluittype_detail_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        resultaattype_url = reverse(
            "resultaattype-detail", kwargs={"uuid": resultaattype.uuid}
        )

        response = self.client.get(besluittype_detail_url)

        expected = {
            "url": f"http://testserver{besluittype_detail_url}",
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "Besluittype",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [],
            "vastgelegdIn": [],
            "beginGeldigheid": "2018-01-01",
            "eindeGeldigheid": None,
            "concept": True,
            "resultaattypen": [f"http://testserver{resultaattype_url}"],
            "beginObject": None,
            "eindeObject": None,
            "resultaattypenOmschrijving": [resultaattype.omschrijving],
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_get_detail_related_informatieobjecttypen(self):
        """Retrieve the details of a single `BesluitType` object with related informatieonnjecttype."""
        besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus, publicatie_indicatie=True
        )
        iot1 = InformatieObjectTypeFactory.create(catalogus=self.catalogus)
        iot2 = InformatieObjectTypeFactory.create(catalogus=self.catalogus)
        besluittype.informatieobjecttypen.add(iot1)

        besluittype_detail_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        iot1_url = reverse("informatieobjecttype-detail", kwargs={"uuid": iot1.uuid})

        response = self.client.get(besluittype_detail_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data["informatieobjecttypen"]), 1)
        self.assertEqual(
            data["informatieobjecttypen"][0], f"http://testserver{iot1_url}"
        )

    def test_get_detail_related_zaaktypen(self):
        """Retrieve the details of a single `BesluitType` object with related zaaktypen."""
        besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus, publicatie_indicatie=True
        )
        zaaktype1 = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype2 = ZaakTypeFactory.create(catalogus=self.catalogus)
        besluittype.zaaktypen.clear()
        besluittype.zaaktypen.add(zaaktype1)

        besluittype_detail_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        zaaktype1_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype1.uuid})

        response = self.client.get(besluittype_detail_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data["zaaktypen"]), 1)
        self.assertEqual(data["zaaktypen"][0], f"http://testserver{zaaktype1_url}")

    def test_create_besluittype(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus
        )
        informatieobjecttype_url = reverse(
            "informatieobjecttype-detail", kwargs={"uuid": informatieobjecttype.uuid}
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        besluittype = BesluitType.objects.get()

        self.assertEqual(besluittype.omschrijving, "test")
        self.assertEqual(besluittype.catalogus, self.catalogus)
        self.assertEqual(besluittype.zaaktypen.get(), zaaktype)
        self.assertEqual(besluittype.informatieobjecttypen.get(), informatieobjecttype)
        self.assertEqual(besluittype.concept, True)

    def test_create_besluittype_fail_non_concept_zaaktypen(self):
        zaaktype = ZaakTypeFactory.create(concept=False, catalogus=self.catalogus)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus
        )
        informatieobjecttype_url = reverse(
            "informatieobjecttype-detail", kwargs={"uuid": informatieobjecttype.uuid}
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptCreateValidator.code)

    def test_create_besluittype_fail_non_concept_informatieobjecttypen(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        informatieobjecttype = InformatieObjectTypeFactory.create(
            concept=False, catalogus=self.catalogus
        )
        informatieobjecttype_url = reverse(
            "informatieobjecttype-detail", kwargs={"uuid": informatieobjecttype.uuid}
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptCreateValidator.code)

    def test_create_besluittype_fail_different_catalogus_for_zaaktypen(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus
        )
        informatieobjecttype_url = reverse(
            "informatieobjecttype-detail", kwargs={"uuid": informatieobjecttype.uuid}
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "relations-incorrect-catalogus")

    def test_create_besluittype_fail_different_catalogus_for_informatieobjecttypen(
        self,
    ):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse(
            "informatieobjecttype-detail", kwargs={"uuid": informatieobjecttype.uuid}
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "relations-incorrect-catalogus")

    def test_publish_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.post(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        besluittype.refresh_from_db()

        self.assertEqual(besluittype.concept, False)

    def test_publish_besluittype_geldigheid(self):

        zaaktype1 = ZaakTypeFactory.create(
            concept=False,
            identificatie="ZAAKTYPE-2018-0000000001",
            datum_begin_geldigheid=date(2018, 1, 1),
        )
        zaaktype2 = ZaakTypeFactory.create(
            concept=True,
            identificatie="ZAAKTYPE-2018-0000000001",
            datum_begin_geldigheid=date(2019, 1, 1),
        )
        besluittype1 = BesluitTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            zaaktypen=[zaaktype1],
        )
        besluittype2 = BesluitTypeFactory.create(
            concept=True,
            omschrijving="foobar",
            zaaktypen=[zaaktype2],
        )

        besluittype_url = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype2.uuid}
        )

        response = self.client.post(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        besluittype1.refresh_from_db()
        besluittype2.refresh_from_db()

        self.assertEqual(besluittype2.concept, False)
        self.assertEqual(
            besluittype1.datum_einde_geldigheid,
            besluittype2.datum_begin_geldigheid - timedelta(days=1),
        )
        self.assertEqual(
            besluittype1.datum_einde_geldigheid,
            besluittype2.datum_begin_geldigheid - timedelta(days=1),
        )
        self.assertEqual(besluittype2.datum_einde_geldigheid, None)

    def test_delete_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.delete(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BesluitType.objects.exists())

    def test_delete_besluittype_fail_not_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.delete(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-object")

    def test_update_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "aangepast",
            "informatieobjecttypen": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.put(besluittype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["toelichting"], "aangepast")

        besluittype.refresh_from_db()
        self.assertEqual(besluittype.toelichting, "aangepast")

    def test_update_besluittype_fail_not_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.put(besluittype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ConceptUpdateValidator.code)

    def test_partial_update_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.patch(besluittype_url, {"toelichting": "ja"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["toelichting"], "ja")

        besluittype.refresh_from_db()
        self.assertEqual(besluittype.toelichting, "ja")

    def test_partial_update_besluittype_fail_not_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.patch(besluittype_url, {"toelichting": "same"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ConceptUpdateValidator.code)

    def test_delete_besluittype_not_related_to_non_concept_resources(self):
        zaaktype = ZaakTypeFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create()

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(**{resource: [related]})
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.delete(besluittype_url)

                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                self.assertFalse(BesluitType.objects.exists())

    def test_delete_besluittype_related_to_non_concept_resource_fails(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(**{resource: [related]})
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.delete(besluittype_url)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, "nonFieldErrors")
                self.assertEqual(error["code"], M2MConceptUpdateValidator.code)

    def test_update_besluittype_not_related_to_non_concept_resource(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(
                    catalogus=catalogus, **{resource: [related]}
                )
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                data = {
                    "catalogus": reverse(catalogus),
                    "zaaktypen": [],
                    "omschrijving": "test",
                    "omschrijvingGeneriek": "",
                    "besluitcategorie": "",
                    "reactietermijn": "P14D",
                    "publicatieIndicatie": True,
                    "publicatietekst": "",
                    "publicatietermijn": None,
                    "toelichting": "aangepast",
                    "informatieobjecttypen": [],
                    "beginGeldigheid": "2019-01-01",
                }
                data[resource] = [reverse(related)]

                response = self.client.put(besluittype_url, data)

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["toelichting"], "aangepast")
                besluittype.delete()

    def test_update_besluittype_related_to_non_concept_resource_fails(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(**{resource: [related]})
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                data = {
                    "catalogus": reverse(catalogus),
                    "zaaktypen": [],
                    "omschrijving": "test",
                    "omschrijvingGeneriek": "",
                    "besluitcategorie": "",
                    "reactietermijn": "P14D",
                    "publicatieIndicatie": True,
                    "publicatietekst": "",
                    "publicatietermijn": None,
                    "toelichting": "aangepast",
                    "informatieobjecttypen": [],
                    "beginGeldigheid": "2019-01-01",
                }
                data[resource] = [reverse(related)]

                response = self.client.put(besluittype_url, data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, "nonFieldErrors")
                self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
                besluittype.delete()

    def test_update_besluittype_add_relation_to_non_concept_resource_fails(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create()
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                data = {
                    "catalogus": reverse(catalogus),
                    "zaaktypen": [],
                    "omschrijving": "test",
                    "omschrijvingGeneriek": "",
                    "besluitcategorie": "",
                    "reactietermijn": "P14D",
                    "publicatieIndicatie": True,
                    "publicatietekst": "",
                    "publicatietermijn": None,
                    "toelichting": "aangepast",
                    "informatieobjecttypen": [],
                    "beginGeldigheid": "2019-01-01",
                }
                data[resource] = [reverse(related)]

                response = self.client.put(besluittype_url, data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, "nonFieldErrors")
                self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
                besluittype.delete()

    def test_partial_update_besluittype_not_related_to_non_concept_resource(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(
                    catalogus=catalogus, **{resource: [related]}
                )
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.patch(
                    besluittype_url, {"toelichting": "aangepast"}
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["toelichting"], "aangepast")
                besluittype.delete()

    def test_partial_update_besluittype_related_to_non_concept_resource_fails(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(
                    catalogus=catalogus, **{resource: [related]}
                )
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.patch(
                    besluittype_url, {"toelichting": "aangepast"}
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, "nonFieldErrors")
                self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
                besluittype.delete()

    def test_partial_update_besluittype_add_relation_to_non_concept_resource_fails(
        self,
    ):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(catalogus=catalogus)
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.patch(
                    besluittype_url, {resource: [reverse(related)]}
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

                error = get_validation_errors(response, "nonFieldErrors")
                self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
                besluittype.delete()

    def test_partial_update_non_concept_besluittype_einde_geldigheid(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(besluittype)

        response = self.client.patch(besluittype_url, {"eindeGeldigheid": "2020-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")

    def test_partial_update_besluittype_einde_geldigheid_related_to_non_concept_resource(
        self,
    ):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypen", "informatieobjecttypen"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypen" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(
                    catalogus=catalogus, **{resource: [related]}
                )
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.patch(
                    besluittype_url, {"eindeGeldigheid": "2020-01-01"}
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")
                besluittype.delete()


class BesluitTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_besluittype_status_alles(self):
        BesluitTypeFactory.create(concept=True, datum_begin_geldigheid=date(2019, 1, 1))
        BesluitTypeFactory.create(concept=False)
        besluittype_list_url = reverse("besluittype-list")

        response = self.client.get(besluittype_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_besluittype_status_concept(self):
        besluittype1 = BesluitTypeFactory.create(concept=True)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        besluittype_list_url = reverse("besluittype-list")
        besluittype1_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype1.uuid}
        )

        response = self.client.get(besluittype_list_url, {"status": "concept"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype1_url}")

    def test_filter_besluittype_status_definitief(self):
        besluittype1 = BesluitTypeFactory.create(concept=True)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        besluittype_list_url = reverse("besluittype-list")
        besluittype2_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype2.uuid}
        )

        response = self.client.get(besluittype_list_url, {"status": "definitief"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype2_url}")

    def test_filter_zaaktypen(self):
        besluittype1 = BesluitTypeFactory.create(concept=False)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        zaaktype1 = besluittype1.zaaktypen.get()
        zaaktype1_url = reverse(zaaktype1)
        besluittype_list_url = reverse("besluittype-list")
        besluittype1_url = reverse(besluittype1)

        response = self.client.get(
            besluittype_list_url, {"zaaktypen": f"http://testserver.com{zaaktype1_url}"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype1_url}")

    def test_filter_informatieobjecttypen(self):
        besluittype1 = BesluitTypeFactory.create(concept=False)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        iot1 = InformatieObjectTypeFactory.create(catalogus=self.catalogus)
        besluittype1.informatieobjecttypen.add(iot1)
        besluittype_list_url = reverse("besluittype-list")
        besluittype1_url = reverse(besluittype1)
        iot1_url = reverse(iot1)

        response = self.client.get(
            besluittype_list_url,
            {"informatieobjecttypen": f"http://testserver.com{iot1_url}"},
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype1_url}")

    def test_filter_omschrijving(self):
        besluittype1 = BesluitTypeFactory.create(concept=False, omschrijving="foobar1")
        besluittype2 = BesluitTypeFactory.create(concept=False, omschrijving="foobar2")
        list_url = get_operation_url("besluittypen_list")
        besluittype1_url = get_operation_url(
            "besluittypen_retrieve", uuid=besluittype1.uuid
        )

        response = self.client.get(
            list_url, {"omschrijving": besluittype1.omschrijving}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype1_url}")

    def test_filter_geldigheid_get_most_recent(self):
        besluittype1 = BesluitTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        besluittype2 = BesluitTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-03-01",
        )
        list_url = get_operation_url("besluittypen_list")

        response = self.client.get(list_url, {"datumGeldigheid": "2020-03-05"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(besluittype2)}")

    def test_filter_geldigheid_get_older_version(self):
        besluittype1 = BesluitTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        besluittype2 = BesluitTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-03-01",
        )
        list_url = get_operation_url("besluittypen_list")

        response = self.client.get(list_url, {"datumGeldigheid": "2020-01-05"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(besluittype1)}")


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        BesluitTypeFactory.create_batch(2)
        besluittype_list_url = get_operation_url("besluittypen_list")

        response = self.client.get(besluittype_list_url, {"someparam": "somevalue"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


class BesluitTypePaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        BesluitTypeFactory.create_batch(2, concept=False)
        besluittype_list_url = reverse("besluittype-list")

        response = self.client.get(besluittype_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        BesluitTypeFactory.create_batch(2, concept=False)
        besluittype_list_url = reverse("besluittype-list")

        response = self.client.get(besluittype_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])


class BesluitTypeValidationTests(APITestCase):
    maxDiff = None

    def test_besluittype_unique_catalogus_omschrijving_combination(self):
        besluittype1 = BesluitTypeFactory(catalogus=self.catalogus, omschrijving="test")
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unique")


class BesluitTypeScopeTests(APITestCase, JWTAuthMixin):
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_FORCED_WRITE]

    def test_update_besluittype_not_concept_with_forced_scope(self):

        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "aangepast",
            "informatieobjecttypen": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.put(besluittype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["toelichting"], "aangepast")

        besluittype.refresh_from_db()
        self.assertEqual(besluittype.toelichting, "aangepast")
