from datetime import date

from django.utils.http import urlencode

from rest_framework import status
from vng_api_common.tests.urls import reverse

from ztc.datamodel.models.zaakobjecttype import ZaakObjectType
from ztc.datamodel.tests.factories.catalogus import CatalogusFactory
from ztc.datamodel.tests.factories.resultaattype import ResultaatTypeFactory
from ztc.datamodel.tests.factories.statustype import StatusTypeFactory
from ztc.datamodel.tests.factories.zaakobjecttype import ZaakObjectTypeFactory
from ztc.datamodel.tests.factories.zaken import ZaakTypeFactory

from .base import APITestCase


class ZaakObjectTypeAPITests(APITestCase):
    def test_list(self):
        """Retrieve a list of `ZaakObjectType` objects."""
        catalogus = CatalogusFactory()
        zaakobjecttype_1 = ZaakObjectTypeFactory(
            catalogus=catalogus,
            datum_begin_geldigheid=date(2021, 11, 18),
        )

        zaakobjecttype_2 = ZaakObjectTypeFactory(
            catalogus=catalogus,
            datum_begin_geldigheid=date(2021, 11, 17),
        )

        response = self.client.get(reverse("zaakobjecttype-list"))
        data = response.json()["results"]

        self.assertEqual(len(data), 2)

        self.assertEqual(
            data[0]["url"], f"http://testserver{reverse(zaakobjecttype_2)}"
        )

        self.assertEqual(
            data[1]["url"], f"http://testserver{reverse(zaakobjecttype_1)}"
        )

    def test_detail(self):
        """Retrieve the details of a single `ZaakObjectType` object."""
        resultaattype = ResultaatTypeFactory()
        statustype = StatusTypeFactory()

        zaakobjecttype = ZaakObjectTypeFactory(
            statustypen=[statustype],
            resultaattypen=[resultaattype],
        )

        response = self.client.get(reverse(zaakobjecttype))
        data = response.json()

        self.assertEqual(data["url"], f"http://testserver{reverse(zaakobjecttype)}")

        self.assertEqual(
            data["statustypen"], [f"http://testserver{reverse(statustype)}"]
        )

        self.assertEqual(
            data["resultaattypen"], [f"http://testserver{reverse(resultaattype)}"]
        )

    def test_create(self):
        """Create a `ZaakObjectType` object."""
        catalogus = CatalogusFactory()
        zaaktype = ZaakTypeFactory(catalogus=catalogus)

        response = self.client.post(
            reverse("zaakobjecttype-list"),
            {
                "anderObjecttype": False,
                "beginGeldigheid": date(2021, 10, 30),
                "eindeGeldigheid": date(2021, 11, 30),
                "objecttype": "https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/abc",
                "relatieOmschrijving": "Test omschrijving",
                "zaaktype": f"http://testserver{reverse(zaaktype)}",
                "catalogus": f"http://testserver{reverse(catalogus)}",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ZaakObjectType.objects.count(), 1)

    def test_update(self):
        """Update a `ZaakObjectType` object."""
        zaakobjecttype = ZaakObjectTypeFactory(
            relatie_omschrijving="Omschrijving 123",
            datum_begin_geldigheid=date(2021, 10, 30),
            datum_einde_geldigheid=date(2021, 11, 30),
        )

        response = self.client.put(
            reverse(zaakobjecttype),
            {
                "anderObjecttype": zaakobjecttype.ander_objecttype,
                "beginGeldigheid": zaakobjecttype.datum_begin_geldigheid,
                "eindeGeldigheid": date(2021, 12, 30),
                "objecttype": zaakobjecttype.objecttype,
                "relatieOmschrijving": "Omschrijving 321",
                "zaaktype": f"http://testserver{reverse(zaakobjecttype.zaaktype)}",
                "catalogus": f"http://testserver{reverse(zaakobjecttype.catalogus)}",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        zaakobjecttype.refresh_from_db()

        self.assertEqual(zaakobjecttype.datum_einde_geldigheid, date(2021, 12, 30))

        self.assertEqual(zaakobjecttype.relatie_omschrijving, "Omschrijving 321")

    def test_partial_update(self):
        """Partially update a `ZaakObjectType` object."""
        zaakobjecttype = ZaakObjectTypeFactory()
        zaaktype = ZaakTypeFactory()

        response = self.client.patch(
            reverse(zaakobjecttype),
            {
                "zaaktype": f"http://testserver{reverse(zaaktype)}",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        zaakobjecttype.refresh_from_db()

        self.assertEqual(zaakobjecttype.zaaktype, zaaktype)

    def test_delete(self):
        """Delete a `ZaakObjectType` object."""
        zaakobjecttype = ZaakObjectTypeFactory()

        response = self.client.delete(reverse(zaakobjecttype))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ZaakObjectType.objects.count(), 0)

    def test_filtering(self):
        """Filter through `ZaakObjectType` objects."""
        zaakobjecttype_1 = ZaakObjectTypeFactory(
            ander_objecttype=True,
            objecttype="https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/abc",
            datum_begin_geldigheid=date(2021, 10, 30),
        )
        ZaakObjectTypeFactory(
            ander_objecttype=True,
            objecttype="https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/bca",
        )
        zaakobjecttype_2 = ZaakObjectTypeFactory(
            ander_objecttype=True,
            objecttype="https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/abc",
            datum_begin_geldigheid=date(2021, 11, 30),
        )
        ZaakObjectTypeFactory(
            ander_objecttype=True,
            objecttype="https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/bca",
        )

        response = self.client.get(
            reverse("zaakobjecttype-list"),
            {
                "anderObjecttype": True,
                "objecttype": (
                    "https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/abc"
                ),
            },
        )

        data = response.json()["results"]

        self.assertEqual(len(data), 2)

        self.assertEqual(
            data[0]["url"], f"http://testserver{reverse(zaakobjecttype_1)}"
        )
        self.assertEqual(
            data[1]["url"], f"http://testserver{reverse(zaakobjecttype_2)}"
        )

    def test_datum_validation(self):
        """
        Ensure datum_begin_geldigheid and datum_einde_geldigheid validation works
        as intended.
        """
        catalogus = CatalogusFactory()
        zaaktype = ZaakTypeFactory(catalogus=catalogus)

        response = self.client.post(
            reverse("zaakobjecttype-list"),
            {
                "anderObjecttype": False,
                "beginGeldigheid": date(2021, 10, 30),
                "eindeGeldigheid": date(2021, 9, 30),
                "objecttype": (
                    "https://bag2.basisregistraties.overheid.nl/bag/id/identificatie/abc"
                ),
                "relatieOmschrijving": "Test omschrijving",
                "zaaktype": f"http://testserver{reverse(zaaktype)}",
                "catalogus": f"http://testserver{reverse(catalogus)}",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_objecttype_validation(self):
        """Ensure objecttype validation works as intended."""
        catalogus = CatalogusFactory()
        zaaktype = ZaakTypeFactory(catalogus=catalogus)

        response = self.client.post(
            reverse("zaakobjecttype-list"),
            {
                "anderObjecttype": False,
                "beginGeldigheid": date(2021, 10, 30),
                "eindeGeldigheid": date(2021, 11, 30),
                "objecttype": "object_type_123",  # URL's are mandatory
                "relatieOmschrijving": "Test omschrijving",
                "zaaktype": f"http://testserver{reverse(zaaktype)}",
                "catalogus": f"http://testserver{reverse(catalogus)}",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
