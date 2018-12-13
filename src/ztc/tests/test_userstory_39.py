"""
Test the flow described in https://github.com/VNG-Realisatie/gemma-zaken/issues/39
"""
from rest_framework import status
from rest_framework.test import APITestCase
from zds_schema.tests import TypeCheckMixin, get_operation_url

from ztc.api.tests.base import ClientAPITestMixin
from ztc.datamodel.tests.factories import StatusTypeFactory, ZaakTypeFactory


class US39TestCase(TypeCheckMixin, ClientAPITestMixin, APITestCase):

    def test_retrieve_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        url = get_operation_url(
            'zaaktype_read',
            catalogus_uuid=zaaktype.catalogus.uuid,
            uuid=zaaktype.uuid
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['url'], f"http://testserver{url}")

        self.assertResponseTypes(response_data, (
            ('identificatie', int),
            ('omschrijving', str),
            ('omschrijvingGeneriek', str),
            ('catalogus', str),
            ('statustypen', list),
        ))

        self.assertIsInstance(response_data['omschrijving'], str)

    def test_retrieve_statustype(self):
        status_type = StatusTypeFactory.create()
        url = get_operation_url(
            'statustype_read',
            catalogus_uuid=status_type.zaaktype.catalogus.uuid,
            zaaktype_uuid=status_type.zaaktype.uuid,
            uuid=status_type.uuid
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['url'], f"http://testserver{url}")

        types = [
            ('omschrijving', str),
            ('omschrijvingGeneriek', str),
            ('statustekst', str),
            ('zaaktype', str),
        ]
        self.assertResponseTypes(response_data, types)
