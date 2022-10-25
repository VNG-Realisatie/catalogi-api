from datetime import date, datetime, timedelta
from unittest import skip

from django.urls import reverse

from rest_framework import status
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.tests import (
    JWTAuthMixin,
    get_operation_url,
    get_validation_errors,
    reverse,
)

from ...datamodel.models import InformatieObjectType
from ...datamodel.tests.factories import (
    BesluitTypeFactory,
    CatalogusFactory,
    InformatieObjectTypeFactory,
    ZaakInformatieobjectTypeFactory,
    ZaakTypeFactory,
)
from ..scopes import (
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ..validators import ConceptUpdateValidator, M2MConceptUpdateValidator
from .base import APITestCase


class InformatieObjectTypeAPITests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_READ]

    def test_get_list_default_definitief(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(concept=True)
        informatieobjecttype2 = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")
        informatieobjecttype2_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype2.uuid
        )

        response = self.client.get(informatieobjecttypen_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["url"], f"http://testserver{informatieobjecttype2_url}"
        )

    def test_get_detail(self):
        """Retrieve the details of a single `InformatieObjectType` object."""

        besluittype = BesluitTypeFactory(catalogus=self.catalogus)
        informatieobjecttype = InformatieObjectTypeFactory(
            catalogus=self.catalogus,
            zaaktypen=None,
            model=["http://www.example.com"],
            trefwoord=["abc", "def"],
            datum_begin_geldigheid="2019-01-01",
            besluittypen=[besluittype],
        )

        zaaktype = ZaakTypeFactory(catalogus=self.catalogus)

        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_detail_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )

        response = self.client.get(informatieobjecttype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            "catalogus": "http://testserver{}".format(self.catalogus_detail_url),
            "omschrijving": informatieobjecttype.omschrijving,
            "url": "http://testserver{}".format(informatieobjecttype_detail_url),
            "vertrouwelijkheidaanduiding": "",
            "beginGeldigheid": "2019-01-01",
            "eindeGeldigheid": None,
            "concept": True,
            "informatieobjectcategorie": "informatieobjectcategorie",
            "trefwoord": ["abc", "def"],
            "zaaktypen": [f"http://testserver{reverse(zaaktype)}"],
            "besluittypen": [f"http://testserver{reverse(besluittype)}"],
            "beginObject": None,
            "eindeObject": None,
            "omschrijvingGeneriek": {
                "definitieInformatieobjecttypeOmschrijvingGeneriek": "",
                "herkomstInformatieobjecttypeOmschrijvingGeneriek": "",
                "hierarchieInformatieobjecttypeOmschrijvingGeneriek": "",
                "informatieobjecttypeOmschrijvingGeneriek": "",
                "opmerkingInformatieobjecttypeOmschrijvingGeneriek": None,
            },
        }
        self.assertEqual(expected, response.json())

    @skip("Not MVP yet")
    def test_is_relevant_voor(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus,
            zaaktypen=None,
            model=["http://www.example.com"],
            trefwoord=["abc", "def"],
        )
        informatieobjecttype_detail_url = get_operation_url(
            "informatieobjecttype_retrieve",
            catalogus_uuid=self.catalogus.uuid,
            uuid=informatieobjecttype.uuid,
        )

        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)

        ziot = ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype,
            informatieobjecttype=informatieobjecttype,
            volgnummer=1,
            richting="richting",
        )

        response = self.client.get(informatieobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue("isRelevantVoor" in data)
        self.assertEqual(len(data["isRelevantVoor"]), 1)
        self.assertEqual(
            data["isRelevantVoor"][0],
            "http://testserver{}".format(
                reverse("zktiot-detail", args=[zaaktype.pk, ziot.pk])
            ),
        )

    @skip("Not MVP yet")
    def test_is_vastlegging_voor(self):
        pass

    def test_create_informatieobjecttype(self):
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.post(informatieobjecttypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        informatieobjecttype = InformatieObjectType.objects.get()

        self.assertEqual(informatieobjecttype.omschrijving, "test")
        self.assertEqual(informatieobjecttype.catalogus, self.catalogus)
        self.assertEqual(informatieobjecttype.concept, True)

    def test_create_informatieobjecttype_fail_not_unique(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        list_url = get_operation_url("informatieobjecttype_list")
        data = {
            "catalogus": f"http://testserver{reverse(informatieobjecttype.catalogus)}",
            "omschrijving": informatieobjecttype.omschrijving,
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unique")

    def test_publish_informatieobjecttype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttypee_url = get_operation_url(
            "informatieobjecttype_publish", uuid=informatieobjecttype.uuid
        )

        response = self.client.post(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        informatieobjecttype.refresh_from_db()

        self.assertEqual(informatieobjecttype.concept, False)

    def test_publish_informatieobjecttype_geldigheid(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(
            concept=False,
            datum_begin_geldigheid=date(2018, 1, 1),
            datum_einde_geldigheid=date(2020, 5, 4),
            omschrijving="foobar",
        )
        informatieobjecttype2 = InformatieObjectTypeFactory.create(
            concept=False,
            datum_begin_geldigheid=date(2020, 5, 5),
            omschrijving="foobar",
        )
        informatieobjecttype3 = InformatieObjectTypeFactory.create(
            concept=True,
            omschrijving="foobar",
            datum_begin_geldigheid=date(2021, 1, 6),
        )

        informatieobjecttypee_url = get_operation_url(
            "informatieobjecttype_publish", uuid=informatieobjecttype3.uuid
        )

        response = self.client.post(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        informatieobjecttype1.refresh_from_db()
        informatieobjecttype2.refresh_from_db()
        informatieobjecttype3.refresh_from_db()

        self.assertEqual(informatieobjecttype3.concept, False)
        self.assertEqual(
            informatieobjecttype2.datum_einde_geldigheid,
            informatieobjecttype3.datum_begin_geldigheid - timedelta(days=1),
        )

        self.assertEqual(
            informatieobjecttype2.datum_einde_geldigheid,
            informatieobjecttype3.datum_begin_geldigheid - timedelta(days=1),
        )
        self.assertEqual(informatieobjecttype3.datum_einde_geldigheid, None)

    def test_publish_informatieobjecttype_overlapping_geldigheid(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(
            concept=False,
            datum_begin_geldigheid=datetime.now().date(),
            omschrijving="foobar",
        )
        informatieobjecttype2 = InformatieObjectTypeFactory.create(
            concept=True, omschrijving="foobar"
        )

        informatieobjecttypee_url = get_operation_url(
            "informatieobjecttype_publish", uuid=informatieobjecttype2.uuid
        )

        response = self.client.post(informatieobjecttypee_url)

        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["code"], "overlapping-geldigheiden")

    def test_delete_informatieobjecttype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttypee_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )

        response = self.client.delete(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            InformatieObjectType.objects.filter(id=informatieobjecttype.id)
        )

    def test_delete_informatieobjecttype_fail_not_concept(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttypee_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )

        response = self.client.delete(informatieobjecttypee_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-object")

    def test_update_informatieobjecttype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "test")

        informatieobjecttype.refresh_from_db()
        self.assertEqual(informatieobjecttype.omschrijving, "test")

    def test_update_informatieobjecttype_fail_not_concept(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ConceptUpdateValidator.code)

    def test_partial_update_informatieobjecttype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(informatieobjecttype_url, {"omschrijving": "ja"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "ja")

        informatieobjecttype.refresh_from_db()
        self.assertEqual(informatieobjecttype.omschrijving, "ja")

    def test_partial_update_informatieobjecttype_fail_not_concept(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(informatieobjecttype_url, {"omschrijving": "same"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ConceptUpdateValidator.code)

    def test_delete_informatieobjecttype_not_related_to_non_concept_zaaktype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()

        zaaktype = ZaakTypeFactory.create()
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.delete(informatieobjecttype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InformatieObjectType.objects.exists())

    def test_delete_informatieobjecttype_not_related_to_non_concept_besluittype(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()

        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype]
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.delete(informatieobjecttype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InformatieObjectType.objects.exists())

    def test_delete_informatieobjecttype_related_to_non_concept_zaaktype_fails(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()

        zaaktype = ZaakTypeFactory.create(concept=False)
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.delete(informatieobjecttype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-relation")

    def test_delete_informatieobjecttype_related_to_non_concept_besluittype_fails(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()

        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype], concept=False
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.delete(informatieobjecttype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-relation")

    def test_update_informatieobjecttype_not_related_to_non_concept_zaaktype(self):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "test")
        informatieobjecttype.delete()

    def test_update_informatieobjecttype_not_related_to_non_concept_besluittype(self):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype], catalogus=catalogus
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "test")
        informatieobjecttype.delete()

    def test_update_informatieobjecttype_related_to_non_concept_zaaktype_fails(self):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        zaaktype = ZaakTypeFactory.create(concept=False, catalogus=catalogus)
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        informatieobjecttype.delete()

    def test_update_informatieobjecttype_related_to_non_concept_besluittype_fails(self):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)

        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype],
            concept=False,
            catalogus=catalogus,
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        informatieobjecttype.delete()

    def test_partial_update_informatieobjecttype_not_related_to_non_concept_zaaktype(
        self,
    ):
        catalogus = CatalogusFactory.create()

        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(informatieobjecttype_url, {"omschrijving": "test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "test")
        informatieobjecttype.delete()

    def test_partial_update_informatieobjecttype_not_related_to_non_concept_besluittype(
        self,
    ):
        catalogus = CatalogusFactory.create()

        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype], catalogus=catalogus
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(informatieobjecttype_url, {"omschrijving": "test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "test")
        informatieobjecttype.delete()

    def test_partial_update_informatieobjecttype_related_to_non_concept_zaaktype_fails(
        self,
    ):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(
            informatieobjecttype_url, {"omschrijving": "aangepast"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        informatieobjecttype.delete()

    def test_partial_update_informatieobjecttype_related_to_non_concept_besluittype_fails(
        self,
    ):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype],
            catalogus=catalogus,
            concept=False,
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(
            informatieobjecttype_url, {"omschrijving": "aangepast"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        informatieobjecttype.delete()

    def test_partial_update_non_concept_informatieobjecttype_einde_geldigheid(self):
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(
            informatieobjecttype_url, {"eindeGeldigheid": "2020-01-01"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")

    def test_partial_update_informatieobjecttype_einde_geldigheid_related_to_non_concept_zaaktype(
        self,
    ):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        zaaktype = ZaakTypeFactory.create(catalogus=catalogus, concept=False)
        ZaakInformatieobjectTypeFactory(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(
            informatieobjecttype_url, {"eindeGeldigheid": "2020-01-01"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")
        informatieobjecttype.delete()

    def test_partial_update_informatieobjecttype_einde_geldigheid_related_to_non_concept_besluittype(
        self,
    ):
        catalogus = CatalogusFactory.create()
        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        besluittype = BesluitTypeFactory.create(
            informatieobjecttypen=[informatieobjecttype],
            catalogus=catalogus,
            concept=False,
        )

        informatieobjecttype_url = reverse(informatieobjecttype)

        response = self.client.patch(
            informatieobjecttype_url, {"eindeGeldigheid": "2020-01-01"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")
        informatieobjecttype.delete()


class InformatieObjectTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_informatieobjecttype_status_alles(self):
        InformatieObjectTypeFactory.create(concept=True)
        InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.get(informatieobjecttypen_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_informatieobjecttype_status_concept(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(concept=True)
        informatieobjecttype2 = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")
        informatieobjecttype1_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype1.uuid
        )

        response = self.client.get(
            informatieobjecttypen_list_url, {"status": "concept"}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["url"], f"http://testserver{informatieobjecttype1_url}"
        )

    def test_filter_informatieobjecttype_status_definitief(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(concept=True)
        informatieobjecttype2 = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")
        informatieobjecttype2_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype2.uuid
        )

        response = self.client.get(
            informatieobjecttypen_list_url, {"status": "definitief"}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["url"], f"http://testserver{informatieobjecttype2_url}"
        )

    def test_filter_omschrijving(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttype2 = InformatieObjectTypeFactory.create(concept=False)
        list_url = get_operation_url("informatieobjecttype_list")
        informatieobjecttype1_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype1.uuid
        )

        response = self.client.get(
            list_url, {"omschrijving": informatieobjecttype1.omschrijving}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["url"], f"http://testserver{informatieobjecttype1_url}"
        )

    def test_filter_geldigheid_get_most_recent(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        informatieobjecttype2 = InformatieObjectTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-03-01",
        )
        list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.get(list_url, {"datumGeldigheid": "2020-03-05"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["beginGeldigheid"], informatieobjecttype2.datum_begin_geldigheid
        )

    def test_filter_geldigheid_get_older_version(self):
        informatieobjecttype1 = InformatieObjectTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        informatieobjecttype2 = InformatieObjectTypeFactory.create(
            concept=False,
            omschrijving="foobar",
            datum_begin_geldigheid="2020-03-01",
        )
        list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.get(list_url, {"datumGeldigheid": "2020-01-05"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["beginGeldigheid"], informatieobjecttype1.datum_begin_geldigheid
        )


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        InformatieObjectTypeFactory.create_batch(2)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.get(
            informatieobjecttypen_list_url, {"someparam": "somevalue"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


class InformatieObjectTypePaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        InformatieObjectTypeFactory.create_batch(2, concept=False)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.get(informatieobjecttypen_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        InformatieObjectTypeFactory.create_batch(2, concept=False)
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.get(informatieobjecttypen_list_url, {"page": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])


class InformatieObjectTypeScopeTests(APITestCase, JWTAuthMixin):
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_FORCED_WRITE]

    def test_update_informatieobjecttype_not_concept_with_forced_scope(self):
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttype_url = reverse(informatieobjecttype)

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2019-01-01",
            "informatieobjectcategorie": "test",
        }

        response = self.client.put(informatieobjecttype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["omschrijving"], "test")

        informatieobjecttype.refresh_from_db()
        self.assertEqual(informatieobjecttype.omschrijving, "test")
