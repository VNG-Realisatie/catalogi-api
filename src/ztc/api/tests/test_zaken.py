import uuid
from datetime import date, datetime, timedelta

from django.test import override_settings
from django.urls import reverse as django_reverse

from rest_framework import status
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.tests import (
    JWTAuthMixin,
    get_operation_url,
    get_validation_errors,
    reverse,
)
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
    EigenschapFactory,
    InformatieObjectTypeFactory,
    ResultaatTypeFactory,
    StatusTypeFactory,
    ZaakInformatieobjectTypeFactory,
    ZaakTypeFactory,
    ZaakTypenRelatieFactory,
)
from ztc.datamodel.tests.factories.zaakobjecttype import ZaakObjectTypeFactory

from ...datamodel.tests.factories import RolTypeFactory
from ..scopes import (
    SCOPE_CATALOGI_FORCED_WRITE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from .base import APITestCase


class ZaakTypeAPITests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_READ]

    def test_get_list_default_definitief(self):
        zaaktype1 = ZaakTypeFactory.create(concept=True)  # noqa
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")
        zaaktype2_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype2.uuid)

        response = self.client.get(zaaktypen_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype2_url}")

    def test_get_detail(self):
        zaaktype = ZaakTypeFactory.create(
            catalogus=self.catalogus,
            verantwoordelijke="Organisatie eenheid X",
            objecttypen=[ZaakObjectTypeFactory(catalogus=self.catalogus)],
            broncatalogus_url="https://catalogus.url/foo",
            broncatalogus_domein="XYZ",
            broncatalogus_rsin="100000000",
            bronzaaktype_url="https://zaaktype.url/foo",
            bronzaaktype_identificatie="1",
            bronzaaktype_omschrijving="omschrijving",
        )
        zaaktype_detail_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype.uuid)
        zaakobjecttype_url = get_operation_url(
            "zaakobjecttype_retrieve", uuid=zaaktype.objecttypen.first().uuid
        )

        response = self.api_client.get(zaaktype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            "url": f"http://testserver{zaaktype_detail_url}",
            "identificatie": zaaktype.identificatie,
            "productenOfDiensten": ["https://example.com/product/123"],
            "publicatieIndicatie": zaaktype.publicatie_indicatie,
            "trefwoorden": [],
            "toelichting": "",
            "handelingInitiator": zaaktype.handeling_initiator,
            "aanleiding": zaaktype.aanleiding,
            "verlengingstermijn": None if not zaaktype.verlenging_mogelijk else "P30D",
            "opschortingEnAanhoudingMogelijk": zaaktype.opschorting_en_aanhouding_mogelijk,
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "indicatieInternOfExtern": zaaktype.indicatie_intern_of_extern,
            "verlengingMogelijk": zaaktype.verlenging_mogelijk,
            "handelingBehandelaar": zaaktype.handeling_behandelaar,
            "doel": zaaktype.doel,
            "onderwerp": zaaktype.onderwerp,
            "publicatietekst": "",
            "omschrijvingGeneriek": "",
            "vertrouwelijkheidaanduiding": "",
            "verantwoordingsrelatie": [],
            "selectielijstProcestype": zaaktype.selectielijst_procestype,
            "servicenorm": None,
            "referentieproces": {"naam": zaaktype.referentieproces_naam, "link": ""},
            "doorlooptijd": "P30D",
            "omschrijving": "",
            "eigenschappen": [],
            "informatieobjecttypen": [],
            "deelzaaktypen": [],
            "gerelateerdeZaaktypen": [],
            "statustypen": [],
            "resultaattypen": [],
            "roltypen": [],
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "eindeGeldigheid": None,
            "beginObject": None,
            "eindeObject": None,
            "versiedatum": "2018-01-01",
            "concept": True,
            "verantwoordelijke": "Organisatie eenheid X",
            "zaakobjecttypen": [f"http://testserver{zaakobjecttype_url}"],
            "broncatalogus": {
                "url": "https://catalogus.url/foo",
                "domein": "XYZ",
                "rsin": "100000000",
            },
            "bronzaaktype": {
                "url": "https://zaaktype.url/foo",
                "identificatie": "1",
                "omschrijving": "omschrijving",
            },
            "beginObject": None,
            "eindeObject": None,
        }
        self.assertEqual(expected, response.json())

    def test_get_detail_404(self):
        ZaakTypeFactory.create(catalogus=self.catalogus)

        url = get_operation_url("zaaktype_retrieve", uuid=uuid.uuid4())

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
        besluittype_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype.uuid
        )

        deelzaaktype1 = ZaakTypeFactory.create(catalogus=self.catalogus, concept=False)
        deelzaaktype2 = ZaakTypeFactory.create(catalogus=self.catalogus, concept=True)

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
            "deelzaaktypen": [
                f"http://testserver{reverse(deelzaaktype1)}",
                f"http://testserver{reverse(deelzaaktype2)}",
            ],
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
            "verantwoordelijke": "Organisatie eenheid X",
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
        self.assertQuerysetEqual(
            zaaktype.deelzaaktypen.all(),
            {deelzaaktype1.pk, deelzaaktype2.pk},
            transform=lambda x: x.pk,
            ordered=False,
        )

    def test_create_zaaktype_fails_no_identificatie(self):
        besluittype = BesluitTypeFactory.create(catalogus=self.catalogus)
        besluittype_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype.uuid
        )

        deelzaaktype1 = ZaakTypeFactory.create(catalogus=self.catalogus, concept=False)
        deelzaaktype2 = ZaakTypeFactory.create(catalogus=self.catalogus, concept=True)

        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
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
            "deelzaaktypen": [
                f"http://testserver{reverse(deelzaaktype1)}",
                f"http://testserver{reverse(deelzaaktype2)}",
            ],
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
            "verantwoordelijke": "Organisatie eenheid X",
        }
        response = self.client.post(zaaktype_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["invalidParams"][0]["code"], "required")

    def test_create_zaaktype_fail_besluittype_non_concept(self):
        besluittype = BesluitTypeFactory.create(concept=False, catalogus=self.catalogus)
        besluittype_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype.uuid
        )

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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptCreateValidator.code)

    def test_create_zaaktype_fail_different_catalogus_zaaktypes(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype.uuid
        )

        zaaktypen_list_url = get_operation_url("zaaktype_list")
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
            "verantwoordelijke": "Organisatie eenheid X",
        }
        response = self.client.post(zaaktypen_list_url, data)

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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "concept-relation")

    def test_publish_zaaktype_fail_not_concept_iotype(self):
        zaaktype = ZaakTypeFactory.create()
        ZaakInformatieobjectTypeFactory.create(zaaktype=zaaktype)

        zaaktype_url = get_operation_url("zaaktype_publish", uuid=zaaktype.uuid)

        response = self.client.post(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "concept-relation")

    def test_publish_zaaktype_fail_concept_deelzaaktype(self):
        deelzaaktype = ZaakTypeFactory.create(concept=True, catalogus=self.catalogus)
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype.deelzaaktypen.add(deelzaaktype)
        publish_url = get_operation_url("zaaktype_publish", uuid=zaaktype.uuid)

        response = self.client.post(publish_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "concept-relation")

    def test_delete_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype.uuid)
        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakType.objects.filter(id=zaaktype.id))

    def test_delete_zaaktype_fail_not_concept(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype.uuid)

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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            catalogus=catalogus, zaaktypen=[zaaktype]
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
            catalogus=catalogus, zaaktypen=[zaaktype], concept=False
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
            catalogus=catalogus, zaaktypen=[zaaktype]
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            catalogus=catalogus, zaaktypen=[zaaktype], concept=False
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
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
            catalogus=catalogus, zaaktypen=[zaaktype]
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
        zaaktype.delete()

    def test_partial_update_zaaktype_not_related_to_non_concept_informatieobjecttype(
        self,
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

    def test_partial_update_zaaktype_related_to_non_concept_besluittype_fails(self):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypen=[zaaktype], concept=False
        )

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], M2MConceptUpdateValidator.code)
        zaaktype.delete()

    def test_partial_update_zaaktype_related_to_non_concept_informatieobjecttype_fails(
        self,
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
        self,
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
            catalogus=catalogus, concept=False, zaaktypen=[zaaktype_for_besluittype]
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

    def test_partial_update_non_concept_zaaktype_reset_einde_geldigheid(self):
        """
        Assert that ``null`` can be set as value for eindeGeldigheid.
        Regression test for https://github.com/open-zaak/open-zaak/issues/981
        """
        zaaktype = ZaakTypeFactory.create(
            concept=False,
            zaaktype_omschrijving="OZ-981",
            identificatie="paspoort",
            datum_begin_geldigheid=date(2021, 1, 1),
            datum_einde_geldigheid=date(2022, 1, 1),
        )
        endpoint = reverse(zaaktype)

        with self.subTest("no overlap"):
            response = self.client.patch(endpoint, {"eindeGeldigheid": None})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            zaaktype.refresh_from_db()
            self.assertIsNone(zaaktype.datum_einde_geldigheid)

        with self.subTest("would introduce overlap"):
            zaaktype_old = ZaakTypeFactory.create(
                concept=False,
                catalogus=zaaktype.catalogus,
                zaaktype_omschrijving="OZ-981",
                identificatie="paspoort",
                datum_begin_geldigheid=date(2020, 1, 1),
                datum_einde_geldigheid=date(2020, 12, 31),
            )

            response = self.client.patch(
                reverse(zaaktype_old), {"eindeGeldigheid": None}
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error = get_validation_errors(response, "eindeGeldigheid")
            self.assertEqual(error["code"], "overlap")

    def test_partial_update_zaaktype_einde_geldigheid_related_to_non_concept_besluittype(
        self,
    ):
        catalogus = CatalogusFactory.create()

        zaaktype = ZaakTypeFactory.create(catalogus=catalogus)
        zaaktype_url = reverse(zaaktype)

        besluittype = BesluitTypeFactory.create(
            catalogus=catalogus, zaaktypen=[zaaktype], concept=False
        )

        response = self.client.patch(zaaktype_url, {"eindeGeldigheid": "2020-01-01"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["einde_geldigheid"], "2020-01-01")
        zaaktype.delete()

    def test_partial_update_zaaktype_einde_geldigheid_related_to_non_concept_informatieobjecttype(
        self,
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

    def test_zaaktype_broncatalogus(self):
        zaaktypen_list_url = get_operation_url("zaaktype_list")

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
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "broncatalogus": {
                "url": "https://catalogus.url/foo",
                "rsin": "222222222",
            },
        }
        response = self.client.post(zaaktypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "broncatalogus.domein")

        self.assertEqual(error["code"], "required")

    def test_zaaktype_bronzaaktype(self):
        zaaktypen_list_url = get_operation_url("zaaktype_list")

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
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "bronzaaktype": {
                "identificatie": "Organisatie",
                "omschrijving": "omschrijving foo",
            },
        }
        response = self.client.post(zaaktypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "bronzaaktype.url")

        self.assertEqual(error["code"], "required")


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
            identificatie=1,
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "beginGeldigheid")
        self.assertEqual(error["code"], "overlap")

    def test_overlap_specified_dates_other_identificatie(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            identificatie=1,
            datum_begin_geldigheid=date(2019, 1, 1),
            datum_einde_geldigheid=date(2020, 1, 1),
            zaaktype_omschrijving="zaaktype",
        )

        data = {
            "omschrijving": "zaaktype",
            "identificatie": 2,
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_overlap_open_end_date(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            identificatie=1,
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "beginGeldigheid")
        self.assertEqual(error["code"], "overlap")

    def test_overlap_open_end_date_other_identificatie(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            identificatie=1,
            datum_begin_geldigheid=date(2019, 1, 1),
            datum_einde_geldigheid=None,
            zaaktype_omschrijving="zaaktype",
        )

        data = {
            "omschrijving": "zaaktype",
            "identificatie": 2,
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_overlap(self):
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            identificatie=1,
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_overlap_exclusive(self):
        """
        Assert that the end date is exclusive.
        """
        ZaakTypeFactory.create(
            catalogus=self.catalogus,
            identificatie=1,
            datum_begin_geldigheid=date(2019, 1, 1),
            datum_einde_geldigheid=date(2020, 1, 1),
            zaaktype_omschrijving="zaaktype",
        )

        data = {
            "omschrijving": "zaaktype",
            "identificatie": 1,
            "catalogus": f"http://testserver{reverse(self.catalogus)}",
            "beginGeldigheid": "2020-01-01",
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ZaakTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_zaaktype_status_alles(self):
        ZaakTypeFactory.create(concept=True)
        ZaakTypeFactory.create(concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktypen_list_url, {"status": "alles"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

    def test_filter_zaaktype_status_concept(self):
        zaaktype1 = ZaakTypeFactory.create(concept=True)
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")
        zaaktype1_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype1.uuid)

        response = self.client.get(zaaktypen_list_url, {"status": "concept"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype1_url}")

    def test_filter_zaaktype_status_definitief(self):
        zaaktype1 = ZaakTypeFactory.create(concept=True)
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")
        zaaktype2_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype2.uuid)

        response = self.client.get(zaaktypen_list_url, {"status": "definitief"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype2_url}")

    def test_filter_identificatie(self):
        zaaktype1 = ZaakTypeFactory.create(concept=False)
        zaaktype2 = ZaakTypeFactory.create(concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")
        zaaktype1_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype1.uuid)

        response = self.client.get(
            zaaktypen_list_url, {"identificatie": zaaktype1.identificatie}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype1_url}")

    def test_filter_geldigheid_get_most_recent(self):
        zaaktype1 = ZaakTypeFactory.create(
            concept=False,
            identificatie=123,
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        zaaktype2 = ZaakTypeFactory.create(
            concept=False,
            identificatie=123,
            datum_begin_geldigheid="2020-03-01",
        )
        zaaktype3 = ZaakTypeFactory.create(
            concept=True,
            identificatie=123,
            datum_begin_geldigheid="2020-03-01",
        )
        zaaktypen_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(
            zaaktypen_list_url, {"datumGeldigheid": "2020-03-05"}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["beginGeldigheid"], zaaktype2.datum_begin_geldigheid)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(zaaktype2)}")

    def test_filter_geldigheid_get_older_version(self):
        zaaktype1 = ZaakTypeFactory.create(
            concept=False,
            identificatie=123,
            datum_begin_geldigheid="2020-01-01",
            datum_einde_geldigheid="2020-02-01",
        )
        zaaktype2 = ZaakTypeFactory.create(
            concept=False,
            identificatie=123,
            datum_begin_geldigheid="2020-03-01",
        )
        zaaktype3 = ZaakTypeFactory.create(
            concept=True,
            identificatie=123,
            datum_begin_geldigheid="2020-03-01",
        )
        zaaktypen_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(
            zaaktypen_list_url, {"datumGeldigheid": "2020-01-05"}
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["beginGeldigheid"], zaaktype1.datum_begin_geldigheid)
        self.assertEqual(data[0]["url"], f"http://testserver{reverse(zaaktype1)}")

    def test_filter_trefwoorden(self):
        zaaktype1 = ZaakTypeFactory.create(
            concept=False, trefwoorden=["some", "key", "words"]
        )
        zaaktype2 = ZaakTypeFactory.create(
            concept=False, trefwoorden=["other", "words"]
        )
        zaaktypen_list_url = get_operation_url("zaaktype_list")
        zaaktype1_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype1.uuid)

        response = self.client.get(zaaktypen_list_url, {"trefwoorden": "key"})
        self.assertEqual(response.status_code, 200)

        data = response.json()["results"]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["url"], f"http://testserver{zaaktype1_url}")

    def test_filter_invalid_resource_url(self):
        ZaakTypeFactory.create()
        url = get_operation_url("zaaktype_list")

        bad_urls = [
            "https://google.nl",
            "https://example.com/",
            "https://example.com/404",
        ]
        for bad_url in bad_urls:
            with self.subTest(bad_url=bad_url):
                response = self.client.get(url, {"catalogus": bad_url})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["count"], 0)


class FilterValidationTests(APITestCase):
    def test_unknown_query_params_give_error(self):
        ZaakTypeFactory.create_batch(2, concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktypen_list_url, {"someparam": "somevalue"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "unknown-parameters")


class ZaakTypePaginationTestCase(APITestCase):
    maxDiff = None

    def test_pagination_default(self):
        ZaakTypeFactory.create_batch(2, concept=False)
        zaaktypen_list_url = get_operation_url("zaaktype_list")

        response = self.client.get(zaaktypen_list_url)

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
        besluittype_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype.uuid
        )

        responses = {
            "http://referentielijsten.nl/procestypen/1234": {
                "some": "incorrect property"
            }
        }

        zaaktypen_list_url = get_operation_url("zaaktype_list")
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
            response = self.client.post(zaaktypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "selectielijstProcestype")
        self.assertEqual(error["code"], "invalid-resource")

    def test_deelzaaktype_different_catalogue(self):
        zaaktype1 = ZaakTypeFactory.create()
        assert zaaktype1.catalogus != self.catalogus
        zaaktype2 = ZaakTypeFactory.create(catalogus=self.catalogus)

        response = self.client.patch(
            reverse(zaaktype2),
            {"deelzaaktypen": [f"http://testserver{reverse(zaaktype1)}"]},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "deelzaaktypen")

        self.assertEqual(error["code"], "relations-incorrect-catalogus")

    def test_create_zaaktype_yields_400_no_verlengingstermijn(self):
        besluittype = BesluitTypeFactory.create(catalogus=self.catalogus)
        besluittype_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype.uuid
        )

        deelzaaktype1 = ZaakTypeFactory.create(catalogus=self.catalogus, concept=False)
        deelzaaktype2 = ZaakTypeFactory.create(catalogus=self.catalogus, concept=True)

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
            "publicatieIndicatie": True,
            "verantwoordingsrelatie": [],
            "productenOfDiensten": ["https://example.com/product/123"],
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "omschrijving": "some test",
            "deelzaaktypen": [
                f"http://testserver{reverse(deelzaaktype1)}",
                f"http://testserver{reverse(deelzaaktype2)}",
            ],
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
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "value-error")
        self.assertEqual(
            error["reason"],
            "'verlengingstermijn' must be set if 'verlenging_mogelijk' is set.",
        )


class ZaakTypeScopeTests(APITestCase, JWTAuthMixin):
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_FORCED_WRITE]

    def test_update_zaaktype_not_concept_with_forced_scope(self):
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
            "besluittypen": [],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
        }
        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["identificatie"], "0")
        self.assertEqual(data["verantwoordelijke"], "Organisatie eenheid X")

        zaaktype.refresh_from_db()
        self.assertEqual(zaaktype.identificatie, "0")

    def test_partial_update_non_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)

        response = self.client.patch(zaaktype_url, {"aanleiding": "aangepast"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")

        zaaktype.refresh_from_db()
        self.assertEqual(zaaktype.aanleiding, "aangepast")
