"""
Test the flow described in https://github.com/VNG-Realisatie/gemma-zaken/issues/39

Zie ook:

* https://github.com/VNG-Realisatie/gemma-zaken/issues/45
"""
from rest_framework import status
from rest_framework.test import APITestCase
from zds_schema.constants import RolOmschrijving
from zds_schema.tests import TypeCheckMixin, get_operation_url

from ztc.api.tests.base import ClientAPITestMixin
from ztc.datamodel.tests.factories import (
    MogelijkeBetrokkeneFactory, RolTypeFactory, ZaakTypeFactory
)


class US169TestCase(TypeCheckMixin, ClientAPITestMixin, APITestCase):

    def test_ophalen_servicenorm_doorlooptijd(self):
        zaaktype = ZaakTypeFactory.create()
        url = get_operation_url(
            'zaaktype_read',
            catalogus_uuid=zaaktype.catalogus.uuid,
            uuid=zaaktype.uuid
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertResponseTypes(response_data, (
            ('doorlooptijd', str),
            ('servicenorm', type(None)),
        ))

        self.assertEqual(response_data['doorlooptijd'], 'P30D')

    def test_ophalen_mogelijke_behandelaars(self):
        """
        Toon aan dat het mogelijk is om een lijst van mogelijke behandelaars
        op te halen.

        Zie https://github.com/VNG-Realisatie/gemma-zaken/issues/182#issuecomment-408899919
        voor context
        """
        zaaktype = ZaakTypeFactory.create()
        roltype_behandelaar = RolTypeFactory.create(
            zaaktype=zaaktype,
            omschrijving_generiek=RolOmschrijving.behandelaar,
        )
        MogelijkeBetrokkeneFactory.create_batch(2, roltype=roltype_behandelaar)

        # unrelated, but same ZAAKTYPE, should not show up
        MogelijkeBetrokkeneFactory.create(
            roltype__zaaktype=zaaktype,
            roltype__omschrijving_generiek=RolOmschrijving.adviseur
        )

        url = get_operation_url(
            'roltype_list',
            catalogus_uuid=zaaktype.catalogus.uuid,
            zaaktype_uuid=zaaktype.uuid
        )

        response = self.client.get(url, {
            'omschrijvingGeneriek': RolOmschrijving.behandelaar,
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(len(response_data), 1)

        self.assertResponseTypes(response_data[0], (
            ('url', str),
            ('zaaktype', str),
            ('omschrijving', str),
            ('omschrijvingGeneriek', str),
            ('mogelijkeBetrokkenen', list),
        ))

        mogelijke_betrokkenen = response_data[0]['mogelijkeBetrokkenen']
        self.assertEqual(len(mogelijke_betrokkenen), 2)

        self.assertResponseTypes(mogelijke_betrokkenen[0], (
            ('betrokkene', str),
            ('betrokkeneType', str),
        ))
