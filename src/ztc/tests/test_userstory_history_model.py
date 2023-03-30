from rest_framework import status
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.tests import get_operation_url, reverse, reverse_lazy

from ztc.api.scopes import (
    SCOPE_CATALOGI_FORCED_DELETE,
    SCOPE_CATALOGI_READ,
    SCOPE_CATALOGI_WRITE,
)
from ztc.api.tests.base import APITestCase
from ztc.datamodel.choices import AardRelatieChoices, InternExtern, RichtingChoices
from ztc.datamodel.models import (
    BesluitType,
    InformatieObjectType,
    ZaakInformatieobjectType,
    ZaakType,
)


class HistoryModelUserStoryTests(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_FORCED_DELETE]

    def test_user_story_new_version_model(self):
        """
        In this userstory the following aspects of the new version model are tested:
        1. POST zaaktype with a besluittypen array consisted of besluittypen_omschrijvingen (which is conventially an array of URI's)
        2. POST besluittypen with a zaaktypen array consisted of zaaktypen_identificatie (which is conventially an array of URI's)
        3. GET a specific zaaktype which contains a list of associated besluittypen. Only the most recent and concept = False besluittypen should be shown.
        """

        self.post_informatieobjecttype()
        self.post_besluittype_1()
        self.post_zaaktype_1()
        self.post_ziot()

        self.publish_besluittype_1()
        self.publish_informatieobject_1()
        self.publish_zaaktype_1()

        self.post_besluittype_2()

        self.publish_besluittype_2()

        self.post_zaaktype_2()
        self.post_ziot_2()

        self.update_zaaktype_2()

        self.publish_zaaktype_2()

        self.delete_besluittype_3()

        self.post_besluittype_3()

        self.get_zaaktype_2()

        self.get_zaaktype_list()

        self.get_besluittype_list()

        self.get_informatieobjecttype()

    def get_zaaktype_list(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        response = self.client.get(zaaktype_list_url)

        besluittype_3 = BesluitType.objects.filter(
            datum_begin_geldigheid="2016-01-01", omschrijving="foo"
        )[0]
        besluittype_4 = BesluitType.objects.filter(
            datum_begin_geldigheid="2016-01-01", omschrijving="foo2"
        )[0]
        besluittype_5 = BesluitType.objects.filter(
            datum_begin_geldigheid="2030-01-01"
        )[0]

        data_zaaktype_2 = response.json()["results"]

        self.assertEqual(
            sorted(data_zaaktype_2[0]["besluittypen"]),
            sorted(
                [
                    f"http://testserver{get_operation_url('besluittype_retrieve', uuid=besluittype_3.uuid)}",
                    f"http://testserver{get_operation_url('besluittype_retrieve', uuid=besluittype_4.uuid)}",
                    f"http://testserver{get_operation_url('besluittype_retrieve', uuid=besluittype_5.uuid)}",

                ]
            ),
        )

    def get_besluittype_list(self):
        besluittype_list_url = get_operation_url("besluittype_list")
        response = self.client.get(besluittype_list_url)

        zaaktype_2 = ZaakType.objects.filter(
            datum_begin_geldigheid="2016-01-01", identificatie="ID"
        )[0]
        data_besluittype = response.json()["results"]

        self.assertEqual(
            sorted(data_besluittype[0]["zaaktypen"]),
            sorted(
                [
                    f"http://testserver{get_operation_url('zaaktype_retrieve', uuid=zaaktype_2.uuid)}"
                ]
            ),
        )

    def post_informatieobjecttype(self):
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "test",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "beginGeldigheid": "2017-01-01",
            "informatieobjectcategorie": "test",
        }
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.post(informatieobjecttypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_besluittype_1(self):
        informatieobjecttype = InformatieObjectType.objects.get()
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "foo",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"{informatieobjecttype.omschrijving}"],
            "beginGeldigheid": "2000-01-01",
            "eindeGeldigheid": "2000-01-02",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

        data2 = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "foo2",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"{informatieobjecttype.omschrijving}"],
            "beginGeldigheid": "2000-01-01",
            "eindeGeldigheid": "2000-01-02",
            "concept": True,
        }

        response_besluit_2 = self.client.post(besluittype_list_url, data2)
        self.assertEqual(response_besluit_2.status_code, 201)

        data3 = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "foo3",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"{informatieobjecttype.omschrijving}"],
            "beginGeldigheid": "2000-01-01",
            "eindeGeldigheid": None,
            "concept": True,
        }

        response_besluit_3 = self.client.post(besluittype_list_url, data3)
        self.assertEqual(response_besluit_3.status_code, 201)

    def post_zaaktype_1(self):
        """
        test if we can post with ' "besluittypen": ["foo"] '. Where "foo" is converted into a URL in the View.
        """
        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "ID",
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
            "gerelateerdeZaaktypen": [],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": ["foo", "foo2"],
            "beginGeldigheid": "2000-01-01",
            "eindeGeldigheid": "2000-01-02",
            # todo normaal staat deze op None, waar word deze gezet bij nieuwe versie van een zaaktype?
            "versiedatum": "2000-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_1 = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response_zaaktype_1.status_code, 201)

    def post_ziot(self):
        list_url = reverse_lazy(ZaakInformatieobjectType)
        zaaktype = ZaakType.objects.get()
        zaaktype_detail_url = get_operation_url("zaaktype_retrieve", uuid=zaaktype.uuid)

        data = {
            "zaaktype": f"http://testserver{zaaktype_detail_url}",
            "informatieobjecttype": "test",
            "volgnummer": 13,
            "richting": RichtingChoices.inkomend,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, 201)

    def post_ziot_2(self):
        list_url = reverse_lazy(ZaakInformatieobjectType)
        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2011-01-01")[0]
        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_2.uuid
        )
        data = {
            "zaaktype": f"http://testserver{zaaktype_detail_url}",
            "informatieobjecttype": "test",
            "volgnummer": 13,
            "richting": RichtingChoices.inkomend,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, 201)

    def publish_besluittype_1(self):
        self.besluittype_1 = BesluitType.objects.all()[0]
        self.besluittype_2 = BesluitType.objects.all()[1]
        self.besluittype_3 = BesluitType.objects.all()[2]

        besluittype_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": self.besluittype_1.uuid}
        )
        response_besluittype_publish = self.client.post(besluittype_url_publish)
        self.assertEqual(response_besluittype_publish.status_code, 200)

        besluittype2_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": self.besluittype_2.uuid}
        )
        response_besluittype2_publish = self.client.post(besluittype2_url_publish)
        self.assertEqual(response_besluittype2_publish.status_code, 200)

        besluittype3_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": self.besluittype_3.uuid}
        )
        response_besluittype3_publish = self.client.post(besluittype3_url_publish)
        self.assertEqual(response_besluittype3_publish.status_code, 200)

    def publish_besluittype_2(self):
        besluittype = BesluitType.objects.filter(datum_begin_geldigheid="2016-01-01")[0]

        besluittype_2 = BesluitType.objects.filter(datum_begin_geldigheid="2016-01-01")[
            1
        ]

        besluittype_url_publish_2 = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype_2.uuid}
        )
        response_besluittype_publish_2 = self.client.post(besluittype_url_publish_2)
        self.assertEqual(response_besluittype_publish_2.status_code, 200)

        besluittype_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype.uuid}
        )
        response_besluittype_publish = self.client.post(besluittype_url_publish)
        self.assertEqual(response_besluittype_publish.status_code, 200)

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
            "identificatie": "ID",
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
                    "zaaktype": "ID",
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

        response_zaaktype_2 = self.client.post(
            zaaktype_list_url, data_2, SERVER_NAME="testserver.com"
        )
        self.assertEqual(response_zaaktype_2.status_code, 201)

    def publish_zaaktype_2(self):
        self.zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2016-01-01")[
            0
        ]
        zaaktype_2_publish = get_operation_url(
            "zaaktype_publish", uuid=self.zaaktype_2.uuid
        )
        response_2_publish = self.client.post(zaaktype_2_publish)
        self.assertEqual(response_2_publish.status_code, status.HTTP_200_OK)

    def post_besluittype_2(self):

        informatieobjecttype = InformatieObjectType.objects.get()
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "foo",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"{informatieobjecttype.omschrijving}"],
            "beginGeldigheid": "2016-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

        data2 = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "zaaktypen": ["ID"],
            "omschrijving": "foo2",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"{informatieobjecttype.omschrijving}"],
            "beginGeldigheid": "2016-01-01",
            "concept": True,
        }

        response_besluit_2 = self.client.post(besluittype_list_url, data2)
        self.assertEqual(response_besluit_2.status_code, 201)

    def post_besluittype_3(self):
        informatieobjecttype = InformatieObjectType.objects.get()
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "foo2",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": [f"{informatieobjecttype.omschrijving}"],
            "beginGeldigheid": "2030-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def get_besluittype_2(self):
        """test that a GET request only returns the most recent associated besluittypen"""

        besluittype_2 = BesluitType.objects.filter(datum_begin_geldigheid="2016-01-01")[
            0
        ]
        besluittype_detail_url = get_operation_url(
            "besluittype_retrieve", uuid=besluittype_2.uuid
        )

        response = self.client.get(besluittype_detail_url)
        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2016-01-01")[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["zaaktypen"]), 1)
        self.assertEqual(
            response.json()["zaaktypen"][0],
            f"http://testserver{get_operation_url('zaaktype_retrieve', uuid=zaaktype_2.uuid)}",
        )

    def get_zaaktype_2(self):
        """test that a GET request only returns the most recent associated besluittypen"""

        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2016-01-01")[0]
        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_2.uuid
        )

        response = self.client.get(zaaktype_detail_url)
        besluittype = BesluitType.objects.filter(datum_begin_geldigheid="2016-01-01")[0]
        besluittype_2 = BesluitType.objects.filter(datum_begin_geldigheid="2016-01-01")[
            1
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["besluittypen"]), 3)

    def get_informatieobjecttype(self):
        informatieobjecttype = InformatieObjectType.objects.get()
        informatieobjecttype_detail_url = get_operation_url(
            "informatieobjecttype_retrieve", uuid=informatieobjecttype.uuid
        )

        response = self.client.get(informatieobjecttype_detail_url)

    def update_zaaktype_2(self):
        zaaktype_2 = ZaakType.objects.filter(datum_begin_geldigheid="2011-01-01")[0]
        zaaktype_url = reverse(zaaktype_2)

        data = {
            "identificatie": "ID",
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
            "besluittypen": ["foo", "foo2", "foo3"],
            "beginGeldigheid": "2016-01-01",
            "versiedatum": "2016-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
        }

        response = self.client.put(zaaktype_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["aanleiding"], "aangepast")

    def delete_besluittype_3(self):
        besluittype = BesluitType.objects.filter(omschrijving="foo3")[0]
        besluittype_url = reverse(besluittype)

        response_besluit_1 = self.client.delete(besluittype_url)

        self.assertEqual(response_besluit_1.status_code, 204)


class HistoryModelMichielScenario1Test(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_FORCED_DELETE]

    def test_user_story_new_version_model(self):
        "====== AANMAKEN OBJECTEN ======"
        self.post_informatieobjecttype()
        self.post_besluittype_1()
        self.post_zaaktype_1()
        self.post_ziot()

        self.publish_besluittype_1()
        self.publish_informatieobject_1()
        self.publish_zaaktype_1()

        self.post_zaaktype_2()
        self.publish_zaaktype_2()

        self.post_zaaktype_3()

        "====== TESTEN SCENARIOS ======"

        self.get_zaaktype_2()

        self.post_zaaktype_1_V2()

        self.get_zaaktype_2_with_updated_Z1()

        self.get_zaaktype_list()

    def post_informatieobjecttype(self):
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "document1",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "beginGeldigheid": "2001-01-01",
            "informatieobjectcategorie": "test",
        }
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.post(informatieobjecttypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_besluittype_1(self):
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "besluittype1",
            "zaaktypen": [],
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": ["document1"],
            "beginGeldigheid": "2000-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def post_zaaktype_1(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "zaaktype1",
            "doel": "some test",
            "aanleiding": "some test",
            "toelichting": "IAM GOING TO CHANGE",
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
            "gerelateerdeZaaktypen": [],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": ["besluittype1"],
            "beginGeldigheid": "2000-01-01",
            "versiedatum": "2000-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_1 = self.client.post(
            zaaktype_list_url, data, SERVER_NAME="testserver.com"
        )

        self.assertEqual(response_zaaktype_1.status_code, 201)

    def post_ziot(self):
        list_url = reverse_lazy(ZaakInformatieobjectType)
        zaaktype = ZaakType.objects.get()
        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype.uuid, SERVER_NAME="testserver.com"
        )

        data = {
            "zaaktype": f"http://testserver{zaaktype_detail_url}",
            "informatieobjecttype": "document1",
            "volgnummer": 13,
            "richting": RichtingChoices.inkomend,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, 201)

    def post_zaaktype_2(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "zaaktype2",
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
                    "zaaktype": "zaaktype1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": [],
            "beginGeldigheid": "2000-01-01",
            "versiedatum": "2000-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_2 = self.client.post(
            zaaktype_list_url, data, SERVER_NAME="testserver.com"
        )

        self.assertEqual(response_zaaktype_2.status_code, 201)

    def post_zaaktype_3(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "zaaktype3",
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
                    "zaaktype": "zaaktype1",
                    "aard_relatie": AardRelatieChoices.bijdrage,
                    "toelichting": "test relations",
                }
            ],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": [],
            "beginGeldigheid": "2000-01-01",
            "versiedatum": "2000-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_3 = self.client.post(
            zaaktype_list_url, data, SERVER_NAME="testserver.com"
        )

        self.assertEqual(response_zaaktype_3.status_code, 201)

    def get_zaaktype_2(self):
        zaaktype_1 = ZaakType.objects.filter(identificatie="zaaktype1")[0]
        zaaktype_2 = ZaakType.objects.filter(identificatie="zaaktype2")[0]
        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_2.uuid
        )

        response = self.client.get(zaaktype_detail_url, SERVER_NAME="testserver.com")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            data["gerelateerdeZaaktypen"][0]["zaaktype"],
            f"http://testserver.com{get_operation_url('zaaktype_retrieve', uuid=zaaktype_1.uuid)}",
        )

        # RESPONSE FOR MICHIEL #todo DELETE THIS BEFORE PRODUCTION DEPLOY

        # URL_ZAAKTYPE_1 = 'http://testserver/api/v1/zaaktypen/cb709c0c-99c2-4298-82ef-4dd76ada9d57'

        #   RESPONSE =
        #   {'aanleiding': 'some test',
        #  'beginGeldigheid': '2000-01-01',
        #  'beginObject': None,
        #  'besluittypen': [],
        #  'broncatalogus': {'domein': None, 'rsin': None, 'url': None},
        #  'bronzaaktype': {'identificatie': None, 'omschrijving': None, 'url': None},
        #  'catalogus': 'http://testserver/api/v1/catalogussen/c998dd98-a387-473e-bbbf-dbec027e265b',
        #  'concept': True,
        #  'deelzaaktypen': [],
        #  'doel': 'some test',
        #  'doorlooptijd': 'P30D',
        #  'eigenschappen': [],
        #  'eindeGeldigheid': None,
        #  'eindeObject': None,
        #  'gerelateerdeZaaktypen': [{'aardRelatie': 'bijdrage',
        #                             'toelichting': 'test relations',
        #                             'zaaktype': 'http://testserver.com/api/v1/zaaktypen/cb709c0c-99c2-4298-82ef-4dd76ada9d57'}],
        #  'handelingBehandelaar': 'uitvoeren',
        #  'handelingInitiator': 'indienen',
        #  'identificatie': 'zaaktype2',
        #  'indicatieInternOfExtern': 'extern',
        #  'informatieobjecttypen': [],
        #  'omschrijving': 'some test',
        #  'omschrijvingGeneriek': '',
        #  'onderwerp': 'Klacht',
        #  'opschortingEnAanhoudingMogelijk': False,
        #  'productenOfDiensten': ['https://example.com/product/123'],
        #  'publicatieIndicatie': True,
        #  'publicatietekst': '',
        #  'referentieproces': {'link': '', 'naam': 'ReferentieProces 0'},
        #  'resultaattypen': [],
        #  'roltypen': [],
        #  'selectielijstProcestype': '',
        #  'servicenorm': None,
        #  'statustypen': [],
        #  'toelichting': '',
        #  'trefwoorden': [],
        #  'url': 'http://testserver/api/v1/zaaktypen/aff5929e-3b7a-4dde-8ee3-41b35ef76af0',
        #  'verantwoordelijke': 'Organisatie eenheid X',
        #  'verantwoordingsrelatie': [],
        #  'verlengingMogelijk': True,
        #  'verlengingstermijn': 'P30D',
        #  'versiedatum': '2000-01-01',
        #  'vertrouwelijkheidaanduiding': 'openbaar',
        #  'zaakobjecttypen': []}

    def post_zaaktype_1_V2(self):
        """Update einde geldigheid zaaktype 1 so we can post a second version of zaaktype 1"""
        zaaktype_1 = ZaakType.objects.filter(identificatie="zaaktype1")[0]
        zaaktype_url = reverse(zaaktype_1)

        data = {
            "eindeGeldigheid": "2003-01-01",
        }

        response = self.client.patch(zaaktype_url, data)
        self.assertEqual(response.status_code, 200)

        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "zaaktype1",
            "doel": "aangepast",
            "aanleiding": "aangepast",
            "toelichting": "IAM A CHANGED ZAAKTYPE",
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
            "gerelateerdeZaaktypen": [],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": [],
            "beginGeldigheid": "2004-01-01",
            "versiedatum": "2004-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_1_v2 = self.client.post(
            zaaktype_list_url, data, SERVER_NAME="testserver.com"
        )

        self.assertEqual(response_zaaktype_1_v2.status_code, 201)

    def publish_besluittype_1(self):
        besluittype = BesluitType.objects.get()

        besluittype_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype.uuid}
        )
        response_besluittype_publish = self.client.post(besluittype_url_publish)
        self.assertEqual(response_besluittype_publish.status_code, 200)

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

    def publish_zaaktype_2(self):
        zaaktype_2 = ZaakType.objects.filter(identificatie="zaaktype2")[0]
        zaaktype_2_publish = get_operation_url("zaaktype_publish", uuid=zaaktype_2.uuid)
        response_2_publish = self.client.post(zaaktype_2_publish)
        self.assertEqual(response_2_publish.status_code, status.HTTP_200_OK)

    def get_zaaktype_2_with_updated_Z1(self):
        zaaktype_1_v2 = ZaakType.objects.filter(
            identificatie="zaaktype1", datum_begin_geldigheid="2004-01-01"
        )[0]
        zaaktype_2 = ZaakType.objects.filter(identificatie="zaaktype2")[0]

        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_2.uuid
        )

        response = self.client.get(zaaktype_detail_url, SERVER_NAME="testserver.com")

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # todo remove with deploy

        # URL_ZAAKTYPE_1_V2 = http://testserver.com/api/v1/zaaktypen/6fdab933-44c5-4b43-87a4-c0cc93c37768

        # response for michiel
        # {'aanleiding': 'some test',
        #  'beginGeldigheid': '2000-01-01',
        #  'beginObject': None,
        #  'besluittypen': [],
        #  'broncatalogus': {'domein': None, 'rsin': None, 'url': None},
        #  'bronzaaktype': {'identificatie': None, 'omschrijving': None, 'url': None},
        #  'catalogus': 'http://testserver.com/api/v1/catalogussen/509bc4bd-f4ab-401b-9b27-ba95e47244a7',
        #  'concept': False,
        #  'deelzaaktypen': [],
        #  'doel': 'some test',
        #  'doorlooptijd': 'P30D',
        #  'eigenschappen': [],
        #  'eindeGeldigheid': None,
        #  'eindeObject': None,
        #  'gerelateerdeZaaktypen': [{'aardRelatie': 'bijdrage',
        #                             'toelichting': 'test relations',
        #                             'zaaktype': 'http://testserver.com/api/v1/zaaktypen/0e64e448-2086-4d62-a188-c4886c7111a6'}],
        #  'handelingBehandelaar': 'uitvoeren',
        #  'handelingInitiator': 'indienen',
        #  'identificatie': 'zaaktype2',
        #  'indicatieInternOfExtern': 'extern',
        #  'informatieobjecttypen': [],
        #  'omschrijving': 'some test',
        #  'omschrijvingGeneriek': '',
        #  'onderwerp': 'Klacht',
        #  'opschortingEnAanhoudingMogelijk': False,
        #  'productenOfDiensten': ['https://example.com/product/123'],
        #  'publicatieIndicatie': True,
        #  'publicatietekst': '',
        #  'referentieproces': {'link': '', 'naam': 'ReferentieProces 0'},
        #  'resultaattypen': [],
        #  'roltypen': [],
        #  'selectielijstProcestype': '',
        #  'servicenorm': None,
        #  'statustypen': [],
        #  'toelichting': '',
        #  'trefwoorden': [],
        #  'url': 'http://testserver.com/api/v1/zaaktypen/a4c661ee-3ef3-4066-81df-b5426fb46cef',
        #  'verantwoordelijke': 'Organisatie eenheid X',
        #  'verantwoordingsrelatie': [],
        #  'verlengingMogelijk': True,
        #  'verlengingstermijn': 'P30D',
        #  'versiedatum': '2000-01-01',
        #  'vertrouwelijkheidaanduiding': 'openbaar',
        #  'zaakobjecttypen': []}

        self.assertEqual(
            data["gerelateerdeZaaktypen"][0]["zaaktype"],
            f"http://testserver.com{get_operation_url('zaaktype_retrieve', uuid=zaaktype_1_v2.uuid)}",
        )

    def get_zaaktype_list(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        response = self.client.get(
            zaaktype_list_url,
            {"datumGeldigheid": "2002-01-01", "identificatie": "zaaktype2"},
            SERVER_NAME="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        data_zaaktype_list = response.json()["results"]

        zaaktype_1_v1 = ZaakType.objects.filter(
            identificatie="zaaktype1", datum_begin_geldigheid="2000-01-01"
        )[0]

        # todo remove with deploy
        # URL_ZAAKTYPE_1_V1 =http://testserver.com/api/v1/zaaktypen/603d5808-aa93-41ad-a1ba-5fabae7d122a

        # response fore michiel
        # [{'aanleiding': 'some test',
        #   'beginGeldigheid': '2000-01-01',
        #   'beginObject': None,
        #   'besluittypen': [],
        #   'broncatalogus': {'domein': None, 'rsin': None, 'url': None},
        #   'bronzaaktype': {'identificatie': None, 'omschrijving': None, 'url': None},
        #   'catalogus': 'http://testserver.com/api/v1/catalogussen/b34197c6-7065-41d7-8234-6b490f2b5da4',
        #   'concept': False,
        #   'deelzaaktypen': [],
        #   'doel': 'some test',
        #   'doorlooptijd': 'P30D',
        #   'eigenschappen': [],
        #   'eindeGeldigheid': None,
        #   'eindeObject': None,
        #   'gerelateerdeZaaktypen': [{'aardRelatie': 'bijdrage',
        #                              'toelichting': 'test relations',
        #                              'zaaktype': 'http://testserver.com/api/v1/zaaktypen/603d5808-aa93-41ad-a1ba-5fabae7d122a'}],
        #   'handelingBehandelaar': 'uitvoeren',
        #   'handelingInitiator': 'indienen',
        #   'identificatie': 'zaaktype2',
        #   'indicatieInternOfExtern': 'extern',
        #   'informatieobjecttypen': [],
        #   'omschrijving': 'some test',
        #   'omschrijvingGeneriek': '',
        #   'onderwerp': 'Klacht',
        #   'opschortingEnAanhoudingMogelijk': False,
        #   'productenOfDiensten': ['https://example.com/product/123'],
        #   'publicatieIndicatie': True,
        #   'publicatietekst': '',
        #   'referentieproces': {'link': '', 'naam': 'ReferentieProces 0'},
        #   'resultaattypen': [],
        #   'roltypen': [],
        #   'selectielijstProcestype': '',
        #   'servicenorm': None,
        #   'statustypen': [],
        #   'toelichting': '',
        #   'trefwoorden': [],
        #   'url': 'http://testserver.com/api/v1/zaaktypen/fffbbf6b-de25-49a6-ad0f-4fd0d9e962cf',
        #   'verantwoordelijke': 'Organisatie eenheid X',
        #   'verantwoordingsrelatie': [],
        #   'verlengingMogelijk': True,
        #   'verlengingstermijn': 'P30D',
        #   'versiedatum': '2000-01-01',
        #   'vertrouwelijkheidaanduiding': 'openbaar',
        #   'zaakobjecttypen': []}]

        self.assertEqual(
            data_zaaktype_list[0]["gerelateerdeZaaktypen"][0]["zaaktype"],
            f"http://testserver.com{get_operation_url('zaaktype_retrieve', uuid=zaaktype_1_v1.uuid)}",
        )


class HistoryModelMichielScenario2Test(APITestCase):
    maxDiff = None
    heeft_alle_autorisaties = False
    scopes = [SCOPE_CATALOGI_READ, SCOPE_CATALOGI_WRITE, SCOPE_CATALOGI_FORCED_DELETE]

    def test_user_story_new_version_model(self):
        "====== AANMAKEN OBJECTEN ======"
        self.post_informatieobjecttype()
        self.post_besluittype_1()
        self.post_zaaktype_1()
        self.post_ziot()

        self.publish_besluittype_1()
        self.publish_informatieobject_1()
        self.publish_zaaktype_1()

        "====== SCENARIO ======"

        self.get_zaaktype_1()
        self.post_besluittype_2()
        self.publish_besluittype_2()
        self.get_zaaktype_1_with_besluittype_1_V2()
        self.get_zaaktype_list()

    def post_informatieobjecttype(self):
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "document1",
            "vertrouwelijkheidaanduiding": VertrouwelijkheidsAanduiding.openbaar,
            "beginGeldigheid": "2001-01-01",
            "informatieobjectcategorie": "test",
        }
        informatieobjecttypen_list_url = get_operation_url("informatieobjecttype_list")

        response = self.client.post(informatieobjecttypen_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_besluittype_1(self):
        besluittype_list_url = reverse("besluittype-list")
        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "besluittype1",
            "zaaktypen": [],
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": ["document1"],
            "beginGeldigheid": "2000-01-01",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def post_zaaktype_1(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        data = {
            "identificatie": "zaaktype1",
            "doel": "some test",
            "aanleiding": "some test",
            "toelichting": "IAM GOING TO CHANGE",
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
            "gerelateerdeZaaktypen": [],
            "referentieproces": {"naam": "ReferentieProces 0", "link": ""},
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "besluittypen": ["besluittype1"],
            "beginGeldigheid": "2000-01-01",
            "versiedatum": "2000-01-01",
            "verantwoordelijke": "Organisatie eenheid X",
            "concept": True,
        }

        response_zaaktype_1 = self.client.post(
            zaaktype_list_url, data, SERVER_NAME="testserver.com"
        )

        self.assertEqual(response_zaaktype_1.status_code, 201)

    def post_ziot(self):
        list_url = reverse_lazy(ZaakInformatieobjectType)
        zaaktype = ZaakType.objects.get()
        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype.uuid, SERVER_NAME="testserver.com"
        )

        data = {
            "zaaktype": f"http://testserver{zaaktype_detail_url}",
            "informatieobjecttype": "document1",
            "volgnummer": 13,
            "richting": RichtingChoices.inkomend,
        }

        response = self.client.post(list_url, data)
        self.assertEqual(response.status_code, 201)

    def publish_besluittype_1(self):
        besluittype = BesluitType.objects.get()

        besluittype_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype.uuid}
        )
        response_besluittype_publish = self.client.post(besluittype_url_publish)
        self.assertEqual(response_besluittype_publish.status_code, 200)

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

    def get_zaaktype_1(self):
        zaaktype_1 = ZaakType.objects.filter(identificatie="zaaktype1")[0]
        besluittype_1 = BesluitType.objects.filter(omschrijving="besluittype1")[0]

        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_1.uuid
        )

        response = self.client.get(zaaktype_detail_url, SERVER_NAME="testserver.com")

        self.assertEqual(response.status_code, 200)

        # todo remove
        # URL_BESLUITTYPE_1 = http://testserver.com/api/v1/besluittypen/75869517-4412-45cf-b427-b3ef1a2fbe13

        # RESPONSE FOR MICHIEL
        # {'aanleiding': 'some test',
        #  'beginGeldigheid': '2000-01-01',
        #  'beginObject': None,
        #  'besluittypen': ['http://testserver.com/api/v1/besluittypen/75869517-4412-45cf-b427-b3ef1a2fbe13'],
        #  'broncatalogus': {'domein': None, 'rsin': None, 'url': None},
        #  'bronzaaktype': {'identificatie': None, 'omschrijving': None, 'url': None},
        #  'catalogus': 'http://testserver.com/api/v1/catalogussen/0e7490d6-7b60-4a1c-91ac-7f06cdc227d8',
        #  'concept': False,
        #  'deelzaaktypen': [],
        #  'doel': 'some test',
        #  'doorlooptijd': 'P30D',
        #  'eigenschappen': [],
        #  'eindeGeldigheid': None,
        #  'eindeObject': None,
        #  'gerelateerdeZaaktypen': [],
        #  'handelingBehandelaar': 'uitvoeren',
        #  'handelingInitiator': 'indienen',
        #  'identificatie': 'zaaktype1',
        #  'indicatieInternOfExtern': 'extern',
        #  'informatieobjecttypen': [
        #      'http://testserver.com/api/v1/informatieobjecttypen/0ca722dc-8595-4cea-a1da-ab8d15b04ca0'],
        #  'omschrijving': 'some test',
        #  'omschrijvingGeneriek': '',
        #  'onderwerp': 'Klacht',
        #  'opschortingEnAanhoudingMogelijk': False,
        #  'productenOfDiensten': ['https://example.com/product/123'],
        #  'publicatieIndicatie': True,
        #  'publicatietekst': '',
        #  'referentieproces': {'link': '', 'naam': 'ReferentieProces 0'},
        #  'resultaattypen': [],
        #  'roltypen': [],
        #  'selectielijstProcestype': '',
        #  'servicenorm': None,
        #  'statustypen': [],
        #  'toelichting': 'IAM GOING TO CHANGE',
        #  'trefwoorden': [],
        #  'url': 'http://testserver.com/api/v1/zaaktypen/3bc5ebf5-c644-4407-bf36-56bfa9c295e2',
        #  'verantwoordelijke': 'Organisatie eenheid X',
        #  'verantwoordingsrelatie': [],
        #  'verlengingMogelijk': True,
        #  'verlengingstermijn': 'P30D',
        #  'versiedatum': '2000-01-01',
        #  'vertrouwelijkheidaanduiding': 'openbaar',
        #  'zaakobjecttypen': []}

    def post_besluittype_2(self):
        besluittype_1 = BesluitType.objects.get()
        besluittype_1_url = reverse(besluittype_1)

        data = {
            "eindeGeldigheid": "2003-01-01",
        }

        response = self.client.patch(besluittype_1_url, data)
        self.assertEqual(response.status_code, 200)

        besluittype_list_url = reverse("besluittype-list")

        data = {
            "catalogus": f"http://testserver{self.catalogus_detail_url}",
            "omschrijving": "besluittype1",
            "omschrijvingGeneriek": "",
            "besluitcategorie": "",
            "reactietermijn": "P14D",
            "publicatieIndicatie": True,
            "publicatietekst": "",
            "publicatietermijn": None,
            "toelichting": "",
            "informatieobjecttypen": ["document1"],
            "beginGeldigheid": "2003-01-02",
            "concept": True,
        }

        response_besluit_1 = self.client.post(besluittype_list_url, data)
        self.assertEqual(response_besluit_1.status_code, 201)

    def publish_besluittype_2(self):
        besluittype = BesluitType.objects.filter(
            omschrijving="besluittype1", datum_begin_geldigheid="2003-01-02"
        )[0]

        besluittype_url_publish = reverse(
            "besluittype-publish", kwargs={"uuid": besluittype.uuid}
        )
        response_besluittype_publish = self.client.post(besluittype_url_publish)
        self.assertEqual(response_besluittype_publish.status_code, 200)

    def get_zaaktype_1_with_besluittype_1_V2(self):
        zaaktype_1 = ZaakType.objects.filter(identificatie="zaaktype1")[0]
        besluittype_1 = BesluitType.objects.filter(
            omschrijving="besluittype1", datum_begin_geldigheid="2003-01-02"
        )[0]

        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_1.uuid
        )

        response = self.client.get(zaaktype_detail_url, SERVER_NAME="testserver.com")

        self.assertEqual(response.status_code, 200)

        # todo remove this
        # UUID_BESLUITTYPE_V2 = 4a51de0c-6c36-4ef7-bd63-134d1d59cb3f

        # RESPONSE FOR MICHIEL
        # {'aanleiding': 'some test',
        #  'beginGeldigheid': '2000-01-01',
        #  'beginObject': None,
        #  'besluittypen': ['http://testserver.com/api/v1/besluittypen/63333f65-9382-43f3-93c0-b091150f9d47'],
        #  'broncatalogus': {'domein': None, 'rsin': None, 'url': None},
        #  'bronzaaktype': {'identificatie': None, 'omschrijving': None, 'url': None},
        #  'catalogus': 'http://testserver.com/api/v1/catalogussen/edcd8451-848d-4272-956c-e351c47321c4',
        #  'concept': False,
        #  'deelzaaktypen': [],
        #  'doel': 'some test',
        #  'doorlooptijd': 'P30D',
        #  'eigenschappen': [],
        #  'eindeGeldigheid': None,
        #  'eindeObject': None,
        #  'gerelateerdeZaaktypen': [],
        #  'handelingBehandelaar': 'uitvoeren',
        #  'handelingInitiator': 'indienen',
        #  'identificatie': 'zaaktype1',
        #  'indicatieInternOfExtern': 'extern',
        #  'informatieobjecttypen': [
        #      'http://testserver.com/api/v1/informatieobjecttypen/b9688c75-45c4-49de-9560-f623aea01ee0'],
        #  'omschrijving': 'some test',
        #  'omschrijvingGeneriek': '',
        #  'onderwerp': 'Klacht',
        #  'opschortingEnAanhoudingMogelijk': False,
        #  'productenOfDiensten': ['https://example.com/product/123'],
        #  'publicatieIndicatie': True,
        #  'publicatietekst': '',
        #  'referentieproces': {'link': '', 'naam': 'ReferentieProces 0'},
        #  'resultaattypen': [],
        #  'roltypen': [],
        #  'selectielijstProcestype': '',
        #  'servicenorm': None,
        #  'statustypen': [],
        #  'toelichting': 'IAM GOING TO CHANGE',
        #  'trefwoorden': [],
        #  'url': 'http://testserver.com/api/v1/zaaktypen/022e1cd5-580f-4479-91c3-a4edede20cb3',
        #  'verantwoordelijke': 'Organisatie eenheid X',
        #  'verantwoordingsrelatie': [],
        #  'verlengingMogelijk': True,
        #  'verlengingstermijn': 'P30D',
        #  'versiedatum': '2000-01-01',
        #  'vertrouwelijkheidaanduiding': 'openbaar',
        #  'zaakobjecttypen': []}

    def get_zaaktype_1_with_besluittype_1_V1(self):
        zaaktype_1 = ZaakType.objects.filter(identificatie="zaaktype1")[0]
        besluittype_1 = BesluitType.objects.filter(
            omschrijving="besluittype1", datum_begin_geldigheid="2003-01-02"
        )[0]

        zaaktype_detail_url = get_operation_url(
            "zaaktype_retrieve", uuid=zaaktype_1.uuid
        )

        response = self.client.get(zaaktype_detail_url, SERVER_NAME="testserver.com")

        self.assertEqual(response.status_code, 200)

    def get_zaaktype_list(self):
        zaaktype_list_url = get_operation_url("zaaktype_list")
        response = self.client.get(
            zaaktype_list_url,
            {"datumGeldigheid": "2000-01-01", "identificatie": "zaaktype1"},
            SERVER_NAME="testserver.com",
        )

        besluittype_v1 = BesluitType.objects.filter(
            omschrijving="besluittype1", datum_begin_geldigheid="2000-01-01"
        )[0]

        self.assertEqual(response.status_code, 200)
        data_zaaktype_list = response.json()["results"]

        zaaktype_1_v1 = ZaakType.objects.filter(
            identificatie="zaaktype1", datum_begin_geldigheid="2000-01-01"
        )[0]

        # todo remove with deploy
        # besluittype_v1_UUID =3f54a1a7-fe15-4cf7-9b6d-1263b3d0c61d

        # RESPONSE FOR MICHIEL
        # {'aanleiding': 'some test',
        #  'beginGeldigheid': '2000-01-01',
        #  'beginObject': None,
        #  'besluittypen': ['http://testserver.com/api/v1/besluittypen/3f54a1a7-fe15-4cf7-9b6d-1263b3d0c61d'],
        #  'broncatalogus': {'domein': None, 'rsin': None, 'url': None},
        #  'bronzaaktype': {'identificatie': None, 'omschrijving': None, 'url': None},
        #  'catalogus': 'http://testserver.com/api/v1/catalogussen/224f9e98-2141-4ecc-a0e9-4e7670b98107',
        #  'concept': False,
        #  'deelzaaktypen': [],
        #  'doel': 'some test',
        #  'doorlooptijd': 'P30D',
        #  'eigenschappen': [],
        #  'eindeGeldigheid': None,
        #  'eindeObject': None,
        #  'gerelateerdeZaaktypen': [],
        #  'handelingBehandelaar': 'uitvoeren',
        #  'handelingInitiator': 'indienen',
        #  'identificatie': 'zaaktype1',
        #  'indicatieInternOfExtern': 'extern',
        #  'informatieobjecttypen': [],
        #  'omschrijving': 'some test',
        #  'omschrijvingGeneriek': '',
        #  'onderwerp': 'Klacht',
        #  'opschortingEnAanhoudingMogelijk': False,
        #  'productenOfDiensten': ['https://example.com/product/123'],
        #  'publicatieIndicatie': True,
        #  'publicatietekst': '',
        #  'referentieproces': {'link': '', 'naam': 'ReferentieProces 0'},
        #  'resultaattypen': [],
        #  'roltypen': [],
        #  'selectielijstProcestype': '',
        #  'servicenorm': None,
        #  'statustypen': [],
        #  'toelichting': 'IAM GOING TO CHANGE',
        #  'trefwoorden': [],
        #  'url': 'http://testserver.com/api/v1/zaaktypen/0c358381-3a0a-43e3-8cda-494848b7d4f7',
        #  'verantwoordelijke': 'Organisatie eenheid X',
        #  'verantwoordingsrelatie': [],
        #  'verlengingMogelijk': True,
        #  'verlengingstermijn': 'P30D',
        #  'versiedatum': '2000-01-01',
        #  'vertrouwelijkheidaanduiding': 'openbaar',
        #  'zaakobjecttypen': []}

        self.assertEqual(
            data_zaaktype_list[0]["besluittypen"][0],
            f"http://testserver.com{get_operation_url('besluittype_retrieve', uuid=besluittype_v1.uuid)}",
        )
