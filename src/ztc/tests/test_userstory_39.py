"""
Test the flow described in https://github.com/VNG-Realisatie/gemma-zaken/issues/39
"""
from rest_framework import status
from rest_framework.test import APITestCase
from zds_schema.tests import get_operation_url

from ztc.api.tests.base import ClientAPITestMixin
from ztc.datamodel.tests.factories import StatusTypeFactory, ZaakTypeFactory


class US39TestCase(ClientAPITestMixin, APITestCase):

    def test_retrieve_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        url = get_operation_url(
            'zaaktype_read',
            catalogus_pk=zaaktype.maakt_deel_uit_van_id,
            id=zaaktype.id
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['url'], f"http://testserver{url}")
        self.assertIsInstance(response_data['omschrijving'], str)

    def test_retrieve_statustype(self):
        status_type = StatusTypeFactory.create()
        url = get_operation_url(
            'zaaktype_read',
            catalogus_pk=status_type.is_van.maakt_deel_uit_van_id,
            zaaktype_pk=status_type.is_van.id,
            id=status_type.id
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['url'], f"http://testserver{url}")
        self.assertIsInstance(response_data['omschrijving'], str)
