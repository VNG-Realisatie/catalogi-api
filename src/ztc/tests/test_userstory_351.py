"""
Test zaak afsluiten
Zie: https://github.com/VNG-Realisatie/gemma-zaken/issues/351
"""
from rest_framework import status
from rest_framework.test import APITestCase
from zds_schema.tests import TypeCheckMixin, get_operation_url

from ztc.api.tests.base import ClientAPITestMixin
from ztc.datamodel.tests.factories import (
    RolTypeFactory, StatusTypeFactory, ZaakTypeFactory
)


class US351TestCase(TypeCheckMixin, ClientAPITestMixin, APITestCase):

    def test_is_eindstatus(self):
        zaaktype = ZaakTypeFactory.create()

        rol_type = RolTypeFactory.create(zaaktype=zaaktype)

        status_type_1 = StatusTypeFactory.create(
            zaaktype=zaaktype,
            roltypen=[rol_type, ],
            statustypevolgnummer=1
        )
        status_type_2 = StatusTypeFactory.create(
            zaaktype=zaaktype,
            roltypen=[rol_type, ],
            statustypevolgnummer=2
        )

        # Volgnummer 1
        url = get_operation_url(
            'statustype_read',
            catalogus_uuid=zaaktype.catalogus.uuid,
            zaaktype_uuid=zaaktype.uuid,
            uuid=status_type_1.uuid,
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertFalse(response_data['isEindstatus'])

        # Volgnummer 2
        url = get_operation_url(
            'statustype_read',
            catalogus_uuid=zaaktype.catalogus.uuid,
            zaaktype_uuid=zaaktype.uuid,
            uuid=status_type_2.uuid
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertTrue(response_data['isEindstatus'])
