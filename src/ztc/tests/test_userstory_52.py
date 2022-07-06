"""
Test that it's possible to read out which extra data needs to be attached
to a ZAAK.
"""
from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import TypeCheckMixin, get_operation_url

from ztc.api.tests.base import ClientAPITestMixin
from ztc.datamodel.choices import FormaatChoices
from ztc.datamodel.tests.factories import (
    EigenschapFactory,
    EigenschapSpecificatieFactory,
    ZaakTypeFactory,
)
from ztc.datamodel.tests.factories.statustype import StatusTypeFactory


class US52TestCase(TypeCheckMixin, ClientAPITestMixin, APITestCase):
    def test_list_eigenschappen(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        statustype = StatusTypeFactory(zaaktype=zaaktype)

        eigenschap1 = EigenschapFactory.create(
            eigenschapnaam="objecttype",
            zaaktype=zaaktype,
            statustype=statustype,
            specificatie_van_eigenschap=EigenschapSpecificatieFactory.create(
                formaat=FormaatChoices.tekst,
                lengte=255,
                kardinaliteit="1",
                waardenverzameling=["boot", "zwerfvuil"],
            ),
            datum_begin_geldigheid=date(2021, 1, 1),
            datum_einde_geldigheid=date(2022, 1, 1),
        )

        EigenschapFactory.create(
            eigenschapnaam="boot.naam",
            zaaktype=zaaktype,
            specificatie_van_eigenschap=EigenschapSpecificatieFactory.create(
                groep="boot",
                formaat=FormaatChoices.tekst,
                lengte=255,
                kardinaliteit="1",
            ),
        )

        EigenschapFactory.create(
            eigenschapnaam="boot.rederij",
            zaaktype=zaaktype,
            specificatie_van_eigenschap=EigenschapSpecificatieFactory.create(
                groep="boot",
                formaat=FormaatChoices.tekst,
                lengte=255,
                kardinaliteit="1",
            ),
        )

        url = get_operation_url(
            "eigenschap_list",
            catalogus_uuid=zaaktype.catalogus.uuid,
            zaaktype_uuid=zaaktype.uuid,
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["results"]

        self.assertEqual(len(response_data), 3)
        self.assertResponseTypes(
            response_data[2],
            {
                ("url", str),
                ("naam", str),
                ("definitie", str),
                ("specificatie", dict),
                ("toelichting", str),
                ("zaaktype", str),
                ("statustype", str),
                ("beginGeldigheid", str),
                ("eindeGeldigheid", str),
            },
        )

        eigenschap_objecttype = next(
            (eig for eig in response_data if eig["naam"] == "objecttype")
        )

        zaaktype_url = get_operation_url(
            "zaaktype_read", catalogus_uuid=zaaktype.catalogus.uuid, uuid=zaaktype.uuid
        )
        statustype_url = get_operation_url("statustype_read", uuid=statustype.uuid)
        detail_url = get_operation_url(
            "eigenschap_read",
            catalogus_uuid=zaaktype.catalogus.uuid,
            zaaktype_uuid=zaaktype.uuid,
            uuid=eigenschap1.uuid,
        )
        self.assertEqual(
            eigenschap_objecttype,
            {
                "url": f"http://testserver{detail_url}",
                "naam": "objecttype",
                "definitie": "",
                "zaaktype": f"http://testserver{zaaktype_url}",
                "toelichting": "",
                "specificatie": {
                    "formaat": FormaatChoices.tekst,
                    "groep": "",
                    "kardinaliteit": "1",
                    "lengte": "255",
                    "waardenverzameling": ["boot", "zwerfvuil"],
                },
                "statustype": f"http://testserver{statustype_url}",
                "beginGeldigheid": "2021-01-01",
                "eindeGeldigheid": "2022-01-01",
                "beginObject": None,
                "eindeObject": None,
                "zaaktypeIdentificatie": zaaktype.identificatie,
            },
        )
