import uuid
from datetime import date
from unittest import skip

from django.test import override_settings
from django.urls import reverse as django_reverse

from rest_framework import status
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.tests import get_operation_url, get_validation_errors, reverse
from zds_client.tests.mocks import mock_client

from ztc.api.validators import (
    ConceptUpdateValidator,
    M2MConceptCreateValidator,
    M2MConceptUpdateValidator,
)
from ztc.datamodel.choices import AardRelatieChoices, InternExtern
from ztc.datamodel.models import ZaakType
from ztc.datamodel.tests.factories import (
    BesluitTypeFactory,
    CatalogusFactory,
    InformatieObjectTypeFactory,
    ZaakInformatieobjectTypeFactory,
    ZaakObjectTypeFactory,
    ZaakTypeFactory,
    ZaakTypenRelatieFactory,
)

from .base import APITestCase


class ZaakTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list_default_definitief(self):
        zaaktype1 = ZaakTypeFactory.create(concept=True)  # noqa
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")
        zaaktype2_url = get_operation_url("zaaktype_read", uuid=zaaktype2.uuid)

        response = self.client.get(zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype2_url}")

    def test_get_detail(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_detail_url = get_operation_url("zaaktype_read", uuid=zaaktype.uuid)

        response = self.api_client.get(zaaktype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            "url": f"http://testserver{zaaktype_detail_url}",
            # 'ingangsdatumObject': '2018-01-01',
            # 'einddatumObject': None,
            "identificatie": zaaktype.zaaktype_identificatie,
            "productenOfDiensten": ["https://example.com/product/123"],
            # 'broncatalogus': None,
            "publicatieIndicatie": zaaktype.publicatie_indicatie,
            "trefwoorden": [],
            # 'zaakcategorie': None,
            "toelichting": "",
            "handelingInitiator": zaaktype.handeling_initiator,
            # 'bronzaaktype': None,
            "aanleiding": zaaktype.aanleiding,
            "verlengingstermijn": None if not zaaktype.verlenging_mogelijk else "P30D",
            "opschortingEnAanhoudingMogelijk": zaaktype.opschorting_en_aanhouding_mogelijk,
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "indicatieInternOfExtern": zaaktype.indicatie_intern_of_extern,
            "verlengingMogelijk": zaaktype.verlenging_mogelijk,
            "handelingBehandelaar": zaaktype.handeling_behandelaar,
            "doel": zaaktype.doel,
            # 'versiedatum': '2018-01-01',
            # 'formulier': [],
            "onderwerp": zaaktype.onderwerp,
            "publicatietekst": "",
            "omschrijvingGeneriek": "",
            "vertrouwelijkheidaanduiding": "",
            "verantwoordingsrelatie": [],
            "selectielijstProcestype": zaaktype.selectielijst_procestype,
            # 'isDeelzaaktypeVan': [],
            "servicenorm": None,
            # 'archiefclassificatiecode': None,
            "referentieproces": {"naam": zaaktype.referentieproces_naam, "link": ""},
            "doorlooptijd": "P30D",
            # 'verantwoordelijke': '',
            "omschrijving": "",
            "eigenschappen": [],
            "informatieobjecttypen": [],
            "gerelateerdeZaaktypen": [],
            # 'heeftRelevantBesluittype': [],
            # 'heeftRelevantZaakObjecttype': [],
            "statustypen": [],
            "resultaattypen": [],
            "roltypen": [],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "eindeGeldigheid": None,
            "versiedatum": "2018-01-01",
            "concept": True,
        }
        self.assertEqual(expected, response.json())

    def test_get_detail_404(self):
        ZaakTypeFactory.create(catalogus=self.catalogus)

        url = get_operation_url("zaaktype_read", uuid=uuid.uuid4())

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        resp_data = response.json()
        del resp_data["instance"]
        self.assertEqual(
            resp_data,
            {
                "code": "not_found",
                "title": "Niet gevonden.",
                "status": 404,
                "detail": "Niet gevonden.",
                "type": "http://testserver{}".format(
                    django_reverse(
                        "vng_api_common:error-detail",
                        kwargs={"exception_class": "NotFound"},
                    )
                ),
            },
        )

    def test_create_zaaktype(self):
        besluittype = BesluitTypeFactory.create(catalogus=self.catalogus)
        besluittype_url = get_operation_url("besluittype_read", uuid=besluittype.uuid)

        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "some test",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [f"http://testserver{besluittype_url}"],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }
        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        zaaktype = ZaakType.objects.get(zaaktype_omschrijving="some test")

        self.assertEqual(zaaktype.catalogus, self.catalogus)
        self.assertEqual(zaaktype.besluittypen.get(), besluittype)
        self.assertEqual(zaaktype.referentieproces_naam, "ReferentieProces 0")
        self.assertEqual(
            zaaktype.zaaktypenrelaties.get().gerelateerd_zaaktype,
            "http://example.com/zaaktype/1",
        )
        self.assertEqual(zaaktype.concept, True)

    def test_create_zaaktype_fail_besluittype_non_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False, catalogus=self.catalogus)
        besluittype_url = get_operation_url("besluittype_read", uuid=besluittype.uuid)

        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "some test",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [f"http://testserver{besluittype_url}"],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptCreateValidator.code)

    def test_create_zaaktype_fail_different_catalogus_zaaktypes(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = get_operation_url("besluittype_read", uuid=besluittype.uuid)

        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "some test",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [f"http://testserver{besluittype_url}"],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }
        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "relations-incorrect-catalogus")

    def test_publish_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        besluittype = BesluitTypeFactory.create(concept=False)
        zaaktype.besluittypen.add(besluittype)
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype__concept=False
        )
        zaaktype_url = get_operation_url("zaaktype_publish", uuid=zaaktype.uuid)

        response = self.client.post(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        zaaktype.refresh_from_db()

        self.assertEqual(zaaktype.concept, False)

    def test_publish_zaaktype_fail_not_concept_besluittype(self):
        zaaktype = ZaakTypeFactory.create()
        besluittype = BesluitTypeFactory.create()
        zaaktype.besluittypen.add(besluittype)

        zaaktype_url = get_operation_url("zaaktype_publish", uuid=zaaktype.uuid)

        response = self.client.post(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data["detail"], "All related resources should be published")

    def test_publish_zaaktype_fail_not_concept_iotype(self):
        zaaktype = ZaakTypeFactory.create()
        ZaakInformatieobjectTypeFactory.create(zaaktype=zaaktype)

        zaaktype_url = get_operation_url("zaaktype_publish", uuid=zaaktype.uuid)

        response = self.client.post(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data["detail"], "All related resources should be published")

    def test_delete_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = get_operation_url("zaaktype_read", uuid=zaaktype.uuid)

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakType.objects.filter(id=zaaktype.id))

    def test_delete_zaaktype_fail_not_concept(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = get_operation_url("zaaktype_read", uuid=zaaktype.uuid)

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-object")

    def test_update_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")

        zaaktype.refresh_from_db()
        self.assertEqual(zaaktype.aanleiding, "aangepast")

    def test_update_zaaktype_fail_not_concept(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ConceptUpdateValidator.code)

    def test_partial_update_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")

        zaaktype.refresh_from_db()
        self.assertEqual(zaaktype.aanleiding, "aangepast")

    def test_partial_update_zaaktype_fail_not_concept(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)

        response = self.client.patch(zaaktype_url, {"aanleiding": "same"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], ConceptUpdateValidator.code)

    def test_delete_zaaktype_not_related_to_non_concept_besluittypen(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype]
        )

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakType.objects.filter(id=zaaktype.id).exists())

    def test_delete_zaaktype_not_related_to_non_concept_informatieobjecttypen(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakType.objects.filter(id=zaaktype.id).exists())

    def test_delete_zaaktype_not_related_to_non_concept_zaaktypes(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        zaaktype2 = ZaakTypeFactory.create(catalogus=catalogus)
        ZaakTypenRelatieFactory.create(
            zaaktype=zaaktype2, gerelateerd_zaaktype=zaaktype
        )

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakType.objects.filter(id=zaaktype.id).exists())

    def test_delete_zaaktype_related_to_non_concept_besluittype_fails(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype], concept=False
        )

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-relation")

    def test_delete_zaaktype_related_to_non_concept_informatieobjecttype_fails(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "non-concept-relation")

    def test_update_zaaktype_not_related_to_non_concept_besluittypen(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype]
        )

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": reverse(catalogus),
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_update_zaaktype_not_related_to_non_concept_informatieobjecttypen(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": reverse(catalogus),
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_update_zaaktype_not_related_to_non_concept_zaaktypes(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        zaaktype2 = ZaakTypeFactory.create(catalogus=catalogus)
        ZaakTypenRelatieFactory.create(
            zaaktype=zaaktype2, gerelateerd_zaaktype=zaaktype
        )

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": reverse(catalogus),
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_update_zaaktype_related_to_non_concept_besluittype_fails(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype], concept=False
        )

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": reverse(catalogus),
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        zaaktype.delete()

    def test_update_zaaktype_related_to_non_concept_informatieobjecttype_fails(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": reverse(catalogus),
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        zaaktype.delete()

    def test_update_zaaktype_add_relation_to_non_concept_besluittype_fails(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "aangepast",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": reverse(catalogus),
            # 'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
        }

        besluittype = BesluitTypeFactory.create(catalogus=catalogus, concept=False)
        data["besluittypen"] = [reverse(besluittype)]

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        zaaktype.delete()

    def test_partial_update_zaaktype_not_related_to_non_concept_besluittype(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(
            catalogus=catalogus, datum_einde_geldigheid="2019-01-01"
        )
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype]
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_partial_update_zaaktype_not_related_to_non_concept_informatieobjecttype(
        self
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(
            catalogus=catalogus, datum_einde_geldigheid="2019-01-01"
        )
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(catalogus=catalogus)
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_partial_update_zaaktype_not_related_to_non_concept_zaaktype(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(
            catalogus=catalogus, datum_einde_geldigheid="2019-01-01"
        )
        zaaktype_url = reverse(zaaktype)

        zaaktype2 = ZaakTypeFactory.create(
            catalogus=catalogus, datum_begin_geldigheid="2020-01-01"
        )
        ZaakTypenRelatieFactory.create(
            zaaktype=zaaktype2, gerelateerd_zaaktype=zaaktype
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_partial_update_zaaktype_related_to_non_concept_informatieobjecttype_fails(
        self
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype], concept=False
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(
            data["detail"],
            "Objects related to non-concept {} can't be updated".format("besluittypen"),
        )
        zaaktype.delete()

    def test_partial_update_zaaktype_related_to_non_concept_informatieobjecttype_fails(
        self
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        zaaktype.delete()

    def test_partial_update_zaaktype_add_relation_to_non_concept_besluittype_fails(
        self
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(
            catalogus=catalogus,
            datum_begin_geldigheid="2018-03-01",
            datum_einde_geldigheid="2019-01-01",
        )
        zaaktype_url = reverse(zaaktype)

        zaaktype_for_besluittype = ZaakTypeFactory.create(
            catalogus=catalogus,
            datum_begin_geldigheid="2015-01-01",
            datum_einde_geldigheid="2016-01-01",
        )
        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, concept=False, zaaktypes=[zaaktype_for_besluittype]
        )
        data = {"besluittypen": [reverse(besluittype)]}

        response = self.client.patch(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        zaaktype.delete()

    def test_partial_update_non_concept_zaaktype_einde_geldigheid(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)

        response = self.client.patch(zaaktype_url, {"eindeGeldigheid": "2020-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")

    def test_partial_update_zaaktype_einde_geldigheid_related_to_non_concept_besluittype(
        self
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypes=[zaaktype], concept=False
        )

        response = self.client.patch(zaaktype_url, {"eindeGeldigheid": "2020-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")
        zaaktype.delete()

    def test_partial_update_zaaktype_einde_geldigheid_related_to_non_concept_informatieobjecttype(
        self
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=catalogus, concept=False
        )
        ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype, informatieobjecttype=informatieobjecttype
        )

        response = self.client.patch(zaaktype_url, {"eindeGeldigheid": "2020-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")
        zaaktype.delete()


class ZaakTypeCreateDuplicateTests(APITestCase):
    """
    Test the creation business rules w/r to duplicates.

    A Zaaktype with the same code is allowed IF and ONLY IF it does not overlap
    in validity period.
    """

    heeft_alle_autorisaties = True

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.catalogus = CatalogusFactory.create()

        cls.url = get_operation_url("zaaktype_list")

    def test_overlap_specified_dates(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            zaaktype_identificatie=1,
            datum_begin_geldigheid=date(2019, 1, 1),
            datum_einde_geldigheid=date(2020, 1, 1),
            zaaktype_omschrijving="zaaktype",
        )

        data = {
            "omschrijving": "zaaktype",
            "identificatie": 1,
            "catalogus": f"http://testserver{reverse(self.catalogus)}",
            "beginGeldigheid": "2019-02-01",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "doel": "doel",
            "aanleiding": "aanleiding",
            "indicatieInternOfExtern": "extern",
            "handelingInitiator": "aanvragen",
            "onderwerp": "dummy",
            "handelingBehandelaar": "behandelen",
            "doorlooptijd": "P7D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": False,
            "publicatieIndicatie": False,
            "productenOfDiensten": [],
            "referentieproces": {"naam": "ref"},
            "besluittypen": [],
            "gerelateerdeZaaktypen": [],
            "versiedatum": "2019-02-01",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "beginGeldigheid")
        self.assertEqual(error["code"], "overlap")

    def test_overlap_open_end_date(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            zaaktype_identificatie=1,
            datum_begin_geldigheid=date(2019, 1, 1),
            datum_einde_geldigheid=None,
            zaaktype_omschrijving="zaaktype",
        )

        data = {
            "omschrijving": "zaaktype",
            "identificatie": 1,
            "catalogus": f"http://testserver{reverse(self.catalogus)}",
            "beginGeldigheid": "2019-02-01",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "doel": "doel",
            "aanleiding": "aanleiding",
            "indicatieInternOfExtern": "extern",
            "handelingInitiator": "aanvragen",
            "onderwerp": "dummy",
            "handelingBehandelaar": "behandelen",
            "doorlooptijd": "P7D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": False,
            "publicatieIndicatie": False,
            "productenOfDiensten": [],
            "referentieproces": {"naam": "ref"},
            "besluittypen": [],
            "gerelateerdeZaaktypen": [],
            "versiedatum": "2019-02-01",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "beginGeldigheid")
        self.assertEqual(error["code"], "overlap")

    def test_no_overlap(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            zaaktype_identificatie=1,
            datum_begin_geldigheid=date(2019, 1, 1),
            datum_einde_geldigheid=date(2020, 1, 1),
            zaaktype_omschrijving="zaaktype",
        )

        data = {
            "omschrijving": "zaaktype",
            "identificatie": 1,
            "catalogus": f"http://testserver{reverse(self.catalogus)}",
            "beginGeldigheid": "2020-02-01",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "doel": "doel",
            "aanleiding": "aanleiding",
            "indicatieInternOfExtern": "extern",
            "handelingInitiator": "aanvragen",
            "onderwerp": "dummy",
            "handelingBehandelaar": "behandelen",
            "doorlooptijd": "P7D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": False,
            "publicatieIndicatie": False,
            "productenOfDiensten": [],
            "referentieproces": {"naam": "ref", "link": "https://example.com"},
            "besluittypen": [],
            "gerelateerdeZaaktypen": [],
            "versiedatum": "2019-02-01",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ZaakTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_zaaktype_status_alles(self):
        ZaakTypeFactory.create(concept=True)
        ZaakTypeFactory.create(concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktype_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_zaaktype_status_concept(self):
        zaaktype1 = ZaakTypeFactory.create(concept=True)
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")
        zaaktype1_url = get_operation_url("zaaktype_read", uuid=zaaktype1.uuid)

        response = self.client.get(zaaktype_list_url, {"status": "concept"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype1_url}")

    def test_filter_zaaktype_status_definitief(self):
        zaaktype1 = ZaakTypeFactory.create(concept=True)
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")
        zaaktype2_url = get_operation_url("zaaktype_read", uuid=zaaktype2.uuid)

        response = self.client.get(zaaktype_list_url, {"status": "definitief"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype2_url}")

    def test_filter_identificatie(self):
        zaaktype1 = ZaakTypeFactory.create(concept=False, zaaktype_identificatie=123)
        zaaktype2 = ZaakTypeFactory.create(concept=False, zaaktype_identificatie=456)
        zaaktype_list_url = get_operation_url("zaaktype_list")
        zaaktype1_url = get_operation_url("zaaktype_read", uuid=zaaktype1.uuid)

        response = self.client.get(zaaktype_list_url, {"identificatie": 123})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype1_url}")

    def test_filter_trefwoorden(self):
        zaaktype1 = ZaakTypeFactory.create(
            concept=False, trefwoorden=["some", "key", "words"]
        )
        zaaktype2 = ZaakTypeFactory.create(
            concept=False, trefwoorden=["other", "words"]
        )
        zaaktype_list_url = get_operation_url("zaaktype_list")
        zaaktype1_url = get_operation_url("zaaktype_read", uuid=zaaktype1.uuid)

        response = self.client.get(zaaktype_list_url, {"trefwoorden": "key"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype1_url}")


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        ZaakTypeFactory.create_batch(2, concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktype_list_url, {"someparam": "somevalue"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


@skip("Not in current MVP")
class ZaakObjectTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.zaakobjecttype = ZaakObjectTypeFactory.create(
            is_relevant_voor__catalogus=self.catalogus
        )

        self.zaaktype = self.zaakobjecttype.is_relevant_voor

        self.zaakobjecttype_list_url = reverse(
            "zaakobjecttype-list",
            kwargs={
                "version": self.API_VERSION,
                "zaaktype_uuid": self.zaaktype.uuid,
                "catalogus_uuid": self.catalogus.uuid,
            },
        )
        self.zaakobjecttype_detail_url = reverse(
            "zaakobjecttype-detail",
            kwargs={
                "version": self.API_VERSION,
                "zaaktype_uuid": self.zaaktype.uuid,
                "catalogus_uuid": self.catalogus.uuid,
                "uuid": self.zaakobjecttype.uuid,
            },
        )

    def test_get_list(self):
        response = self.api_client.get(self.zaakobjecttype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue("results" in data)
        self.assertEqual(len(data["results"]), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.zaakobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            "anderObject": "",
            "einddatumObject": None,
            "ingangsdatumObject": "2018-01-01",
            "isRelevantVoor": "http://testserver{}".format(
                reverse(
                    "zaaktype-detail",
                    args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk],
                )
            ),
            "objecttype": "",
            "relatieOmschrijving": "",
            "url": "http://testserver{}".format(self.zaakobjecttype_detail_url),
        }
        self.assertEqual(expected, response.json())


class ZaakTypePaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        ZaakTypeFactory.create_batch(2, concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktype_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        ZaakTypeFactory.create_batch(2, concept=False)
        zaaktype_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktype_list_url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])


class ZaaktypeValidationTests(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.catalogus = CatalogusFactory.create()

        cls.url = get_operation_url("zaaktype_list")

    @override_settings(LINK_FETCHER="vng_api_common.mocks.link_fetcher_200")
    def test_selectielijstprocestype_invalid_resource(self):
        besluittype = BesluitTypeFactory.create(catalogus=self.catalogus)
        besluittype_url = get_operation_url("besluittype_read", uuid=besluittype.uuid)

        responses = {
            "http://referentielijsten.nl/procestypen/1234": {
                "some": "incorrect property"
            }
        }

        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": 0,
            "doel": "some test",
            "aanleiding": "some test",
            "indicatieInternOfExtern": InternExtern.extern,
            "handelingInitiator": "indienen",
            "onderwerp": "Klacht",
            "handelingBehandelaar": "uitvoeren",
            "doorlooptijd": "P30D",
            "opschortingEnAanhoudingMogelijk": False,
            "verlengingMogelijk": True,
            "verlengingstermijn": "P30D",
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "gerelateerdeZaaktypen": [
                {
                    "zaaktype": "http://example.com/zaaktype/1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": [f"http://testserver{besluittype_url}"],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "selectielijstProcestype": "http://referentielijsten.nl/procestypen/1234",
        }

        with mock_client(responses):
            response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "selectielijstProcestype")
        self.assertEqual(error["code"], "invalid-resource")
