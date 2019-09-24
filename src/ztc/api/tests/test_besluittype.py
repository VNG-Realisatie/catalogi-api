from rest_framework import status
from vng_api_common.tests import get_operation_url, get_validation_errors, reverse
from vng_api_common.utils import underscore_to_camel

from ...datamodel.models import BesluitType
from ...datamodel.tests.factories import (
    BesluitTypeFactory,
    InformatieObjectTypeFactory,
    ZaakTypeFactory,
    CatalogusFactory,
)
from .base import APITestCase


class BesluitTypeAPITests(APITestCase):
    maxDiff = None

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
        besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus, publicatie_indicatie=True
        )
        zaaktype = besluittype.zaaktypes.get()
        zaaktype_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype.uuid})
        besluittype_detail_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        # resultaattype_url = reverse('resultaattype-detail', kwargs={
        #     'catalogus_uuid': self.catalogus.uuid,
        #     'zaaktype_uuid': self.zaaktype.uuid,
        #     'uuid': self.resultaattype.uuid,
        # })

        response = self.client.get(besluittype_detail_url)

        self.assertEqual(response.status_code, 200)
        expected = {
            "url": f"http://testserver{besluittype_detail_url}",
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypes": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "Besluittype",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [],
            "beginGeldigheid": "2018-01-01",
            "eindeGeldigheid": None,
            "concept": True,
            # 'resultaattypes': ['http://testserver{resultaattype_url}'],
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail_related_informatieobjecttypes(self):
        """Retrieve the details of a single `BesluitType` object with related informatieonnjecttype."""
        besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus, publicatie_indicatie=True
        )
        iot1 = InformatieObjectTypeFactory.create(catalogus=self.catalogus)
        iot2 = InformatieObjectTypeFactory.create(catalogus=self.catalogus)
        besluittype.informatieobjecttypes.add(iot1)

        besluittype_detail_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        iot1_url = reverse("informatieobjecttype-detail", kwargs={"uuid": iot1.uuid})

        response = self.client.get(besluittype_detail_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data["informatieobjecttypes"]), 1)
        self.assertEqual(
            data["informatieobjecttypes"][0], f"http://testserver{iot1_url}"
        )

    def test_get_detail_related_zaaktypes(self):
        """Retrieve the details of a single `BesluitType` object with related zaaktypes."""
        besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus, publicatie_indicatie=True
        )
        zaaktype1 = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype2 = ZaakTypeFactory.create(catalogus=self.catalogus)
        besluittype.zaaktypes.clear()
        besluittype.zaaktypes.add(zaaktype1)

        besluittype_detail_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        zaaktype1_url = reverse("zaaktype-detail", kwargs={"uuid": zaaktype1.uuid})

        response = self.client.get(besluittype_detail_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data["zaaktypes"]), 1)
        self.assertEqual(data["zaaktypes"][0], f"http://testserver{zaaktype1_url}")

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
            "zaaktypes": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        besluittype = BesluitType.objects.get()

        self.assertEqual(besluittype.omschrijving, "test")
        self.assertEqual(besluittype.catalogus, self.catalogus)
        self.assertEqual(besluittype.zaaktypes.get(), zaaktype)
        self.assertEqual(besluittype.informatieobjecttypes.get(), informatieobjecttype)
        self.assertEqual(besluittype.concept, True)

    def test_create_besluittype_fail_non_concept_zaaktypes(self):
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
            "zaaktypes": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(
            data["detail"], "Relations to non-concept zaaktypes object can't be created"
        )

    def test_create_besluittype_fail_non_concept_informatieobjecttypes(self):
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
            "zaaktypes": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(
            data["detail"],
            "Relations to non-concept informatieobjecttypes object can't be created",
        )

    def test_create_besluittype_fail_different_catalogus_for_zaaktypes(self):
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
            "zaaktypes": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [f"http://testserver{informatieobjecttype_url}"],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "relations-incorrect-catalogus")

    def test_create_besluittype_fail_different_catalogus_for_informatieobjecttypes(
        self
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
            "zaaktypes": [f"http://testserver{zaaktype_url}"],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [f"http://testserver{informatieobjecttype_url}"],
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data["detail"], "Alleen concepten kunnen worden verwijderd.")

    def test_update_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypes": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "aangepast",
            "informatieobjecttypes": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.put(besluittype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["toelichting"], "aangepast")

    def test_update_besluittype_fail_not_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypes": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.put(besluittype_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data["detail"], "Alleen concepten kunnen worden bijgewerkt.")

    def test_partial_update_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.patch(besluittype_url, {"toelichting": "ja"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["toelichting"], "ja")

    def test_partial_update_besluittype_fail_not_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False)
        besluittype_url = reverse(
            "besluittype-detail", kwargs={"uuid": besluittype.uuid}
        )

        response = self.client.patch(besluittype_url, {"toelichting": "same"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data["detail"], "Alleen concepten kunnen worden bijgewerkt.")

    def test_delete_besluittype_not_related_to_non_concept_resources(self):
        zaaktype = ZaakTypeFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create()

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
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

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(**{resource: [related]})
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.delete(besluittype_url)

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

                data = response.json()
                self.assertEqual(
                    data["detail"],
                    "Objects related to non-concept {} can't be destroyed".format(
                        resource
                    ),
                )

    def test_update_besluittype_not_related_to_non_concept_resource(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(
                    catalogus=catalogus, **{resource: [related]}
                )
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                data = {
                    "catalogus": reverse(catalogus),
                    "zaaktypes": [],
                    "omschrijving": "test",
                    "omschrijvingGeneriek": "",
                    "besluitcategorie": "",
                    "reactietermijn": "P14D",
                    "publicatieIndicatie": True,
                    "publicatietekst": "",
                    "publicatietermijn": None,
                    "toelichting": "aangepast",
                    "informatieobjecttypes": [],
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

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(**{resource: [related]})
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                data = {
                    "catalogus": reverse(catalogus),
                    "zaaktypes": [],
                    "omschrijving": "test",
                    "omschrijvingGeneriek": "",
                    "besluitcategorie": "",
                    "reactietermijn": "P14D",
                    "publicatieIndicatie": True,
                    "publicatietekst": "",
                    "publicatietermijn": None,
                    "toelichting": "aangepast",
                    "informatieobjecttypes": [],
                    "beginGeldigheid": "2019-01-01",
                }
                data[resource] = [reverse(related)]

                response = self.client.put(besluittype_url, data)

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

                data = response.json()
                self.assertEqual(
                    data["detail"],
                    "Objects related to non-concept {} can't be updated".format(
                        resource
                    ),
                )
                besluittype.delete()

    def test_update_besluittype_add_relation_to_non_concept_resource_fails(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
                besluittype = BesluitTypeFactory.create()
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                data = {
                    "catalogus": reverse(catalogus),
                    "zaaktypes": [],
                    "omschrijving": "test",
                    "omschrijvingGeneriek": "",
                    "besluitcategorie": "",
                    "reactietermijn": "P14D",
                    "publicatieIndicatie": True,
                    "publicatietekst": "",
                    "publicatietermijn": None,
                    "toelichting": "aangepast",
                    "informatieobjecttypes": [],
                    "beginGeldigheid": "2019-01-01",
                }
                data[resource] = [reverse(related)]

                response = self.client.put(besluittype_url, data)

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

                data = response.json()
                self.assertEqual(
                    data["detail"],
                    "Objects can't be updated with a relation to non-concept {}".format(
                        resource
                    ),
                )
                besluittype.delete()

    def test_partial_update_besluittype_not_related_to_non_concept_resource(self):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
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

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(
                    catalogus=catalogus, **{resource: [related]}
                )
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.patch(
                    besluittype_url, {"toelichting": "aangepast"}
                )

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

                data = response.json()
                self.assertEqual(
                    data["detail"],
                    "Objects related to non-concept {} can't be updated".format(
                        resource
                    ),
                )
                besluittype.delete()

    def test_partial_update_besluittype_add_relation_to_non_concept_resource_fails(
        self
    ):
        catalogus = CatalogusFactory.create()
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )

        for resource in ["zaaktypes", "informatieobjecttypes"]:
            with self.subTest(resource=resource):
                related = zaaktype if resource == "zaaktypes" else informatieobjecttype
                besluittype = BesluitTypeFactory.create(catalogus=catalogus)
                besluittype_url = reverse(
                    "besluittype-detail", kwargs={"uuid": besluittype.uuid}
                )

                response = self.client.patch(
                    besluittype_url, {resource: [reverse(related)]}
                )

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

                data = response.json()
                self.assertEqual(
                    data["detail"],
                    "Objects can't be updated with a relation to non-concept {}".format(
                        resource
                    ),
                )
                besluittype.delete()


class BesluitTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_besluittype_status_alles(self):
        BesluitTypeFactory.create(concept=True)
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

    def test_filter_zaaktypes(self):
        besluittype1 = BesluitTypeFactory.create(concept=False)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        zaaktype1 = besluittype1.zaaktypes.get()
        zaaktype1_url = reverse(zaaktype1)
        besluittype_list_url = reverse("besluittype-list")
        besluittype1_url = reverse(besluittype1)

        response = self.client.get(besluittype_list_url, {"zaaktypes": zaaktype1_url})

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype1_url}")

    def test_filter_informatieobjecttypes(self):
        besluittype1 = BesluitTypeFactory.create(concept=False)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        iot1 = InformatieObjectTypeFactory.create(catalogus=self.catalogus)
        besluittype1.informatieobjecttypes.add(iot1)
        besluittype_list_url = reverse("besluittype-list")
        besluittype1_url = reverse(besluittype1)
        iot1_url = reverse(iot1)

        response = self.client.get(
            besluittype_list_url, {"informatieobjecttypes": iot1_url}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{besluittype1_url}")


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        BesluitTypeFactory.create_batch(2)
        besluittype_list_url = get_operation_url("besluittype_list")

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
            "zaaktypes": [],
            "omschrijving": "test",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypes": [],
            "beginGeldigheid": "2019-01-01",
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unique")


class BesluittypeConceptTests(APITestCase):
    def test_delete_concept_not_permitted(self):
        besluittype1 = BesluitTypeFactory.create(concept=False)
        besluittype2 = BesluitTypeFactory.create(concept=False)
        zaaktype1 = besluittype1.zaaktypes.get()
        zaaktype1_url = reverse(zaaktype1)
