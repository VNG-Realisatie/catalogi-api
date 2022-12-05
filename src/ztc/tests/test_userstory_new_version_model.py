from rest_framework import status
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.tests import get_operation_url, reverse

from ztc.api.scopes import SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE
from ztc.api.tests.base import APITestCase
from ztc.datamodel.choices import AardRelatieChoices, InternExtern
from ztc.datamodel.models import BesluitType, InformatieObjectType, ZaakType


class BesluitTypeAPITests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE]

    def test_userstory_new_version_model(self):
        """
        In this userstory the following aspects of the new version model are tested:
        1. POST zaaktype with a besluittypen array consisted of besluittypen_omschrijvingen (which is conventially an array of URI's)
        2. POST besluittypen with a zaaktypen array consisted of zaaktypen_identificatie (which is conventially an array of URI's)
        3. GET a specific zaaktype which contains a list of associated besluittypen. Only the most recent and concept = False besluittypen should be shown.

        """
        self.post_informatieobjecttype()
        self.post_besluittype_1()
        self.post_zaaktype_1()

        self.publish_besluittype_1()
        self.publish_informatieobject_1()
        self.publish_zaaktype_1()

        self.post_zaaktype_2()
        self.update_zaaktype_2()
        self.publish_zaaktype_2()
        self.post_besluittype_2()
        self.publish_besluittype_2()

        self.post_besluittype_3()

        self.get_zaaktype_2()

    def post_informatieobjecttype(self):
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "beginGeldigheid": "2000-01-01",
            "informatieobjectcategorie": "test",
        }
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.post(informatieobjecttypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_besluittype_1(self):
        informatieobjecttype = InformatieObjectType.objects.get()
        informatieobjecttype_detail_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "foo",
            "zaaktypen": [],
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [
                f"http://testserver{informatieobjecttype_detail_url}"
            ],
            "beginGeldigheid": "2000-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def post_zaaktype_1(self):
        """
        test if we can post with ' "besluittypen": ["foo"] '. Where "foo" is converted into a URL in the View.
        """
        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "0",
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
            "besluittypen": ["foo"],
            "beginGeldigheid": "2000-01-01",
            "versiedatum": "2000-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_1 = self.client.post(zaaktype_list_url, data)
        self.assertEqual(response_zaaktype_1.status_code, 201)
        zaaktype_1 = ZaakType.objects.all().first()

    def publish_besluittype_1(self):
        self.besluittype_1 = BesluitType.objects.all().first()

        besluittype_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": self.besluittype_1.uuid}
        )
        response_besluittype_publish = self.client.post(besluittype_url_publish)
        self.assertEqual(response_besluittype_publish.status_code, 200)

    def publish_besluittype_2(self):
        self.besluittype_2 = BesluitType.objects.filter(
            datum_begin_geldigheid="2016-01-01"
        )[0]

        besluittype_url_publish_2 = reverse(
            "besluittype-publish", kwargs={"uuid": self.besluittype_2.uuid}
        )
        response_besluittype_publish_2 = self.client.post(besluittype_url_publish_2)
        self.assertEqual(response_besluittype_publish_2.status_code, 200)

    def publish_informatieobject_1(self):
        informatieobjecttype = InformatieObjectType.objects.get()

        informatieobjecttypee_url = get_operation_url(
            "informatieobjecttype_publish", uuid=informatieobjecttype.uuid
        )

        response_informatieobjecttypee_url = self.client.post(informatieobjecttypee_url)

        self.assertEqual(
            response_informatieobjecttypee_url.status_code, status.HTTP_200_OK
        )

    def publish_zaaktype_1(self):
        zaaktype_1 = ZaakType.objects.all().first()
        zaaktype_1_publish = get_operation_url("zaaktype_publish", uuid=zaaktype_1.uuid)
        response_1_publish = self.client.post(zaaktype_1_publish)
        self.assertEqual(response_1_publish.status_code, status.HTTP_200_OK)

    def post_zaaktype_2(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")

        data_2 = {
            "identificatie": "0",
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
            "besluittypen": [f"foo"],
            "beginGeldigheid": "2011-01-01",
            "versiedatum": "2011-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_2 = self.client.post(zaaktype_list_url, data_2)
        self.assertEqual(response_zaaktype_2.status_code, 201)

    def publish_zaaktype_2(self):
        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2018-01-01")[0]
        zaaktype_2_publish = get_operation_url("zaaktype_publish", uuid=zaaktype_2.uuid)
        response_2_publish = self.client.post(zaaktype_2_publish)
        self.assertEqual(response_2_publish.status_code, status.HTTP_200_OK)

    def post_besluittype_2(self):
        """
        test if we can post with ' "zaaktypen": ["0"], '. Where "0" is converted into a URL in the View.
        """

        informatieobjecttype = InformatieObjectType.objects.get()
        informatieobjecttype_detail_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": ["0"],
            "omschrijving": "foo",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [
                f"http://testserver{informatieobjecttype_detail_url}"
            ],
            "beginGeldigheid": "2016-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def post_besluittype_3(self):
        informatieobjecttype = InformatieObjectType.objects.get()
        informatieobjecttype_detail_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": [f"0"],
            "omschrijving": "foo",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [
                f"http://testserver{informatieobjecttype_detail_url}"
            ],
            "beginGeldigheid": "2030-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def get_zaaktype_2(self):
        """test that a GET request only returns the most recent associated besluittypen with concept=False"""

        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2018-01-01")[0]
        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_2.uuid
        )

        response = self.client.get(zaaktype_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["besluittypen"]), 1)
        self.assertEqual(
            response.json()["besluittypen"][0],
            f"http://testserver{get_operation_url('besluittype_retrieve', uuid=self.besluittype_2.uuid)}",
        )

    def update_zaaktype_2(self):
        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2011-01-01")[0]
        zaaktype_url = reverse(zaaktype_2)

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
                    "zaaktype": "http://example.com/zaaktype/2",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": ["foo"],
            "beginGeldigheid": "2018-01-01",
            "versiedatum": "2018-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")
