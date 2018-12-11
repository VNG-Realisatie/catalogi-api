from unittest import skip

from django.urls import reverse

from zds_schema.tests import get_operation_url

from ...datamodel.tests.factories import (
    InformatieObjectTypeFactory, ZaakInformatieobjectTypeFactory,
    ZaakTypeFactory
)
from .base import APITestCase


class InformatieObjectTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.informatieobjecttype = InformatieObjectTypeFactory.create(
            catalogus=self.catalogus,
            zaaktypes=None,
            model=['http://www.example.com'],
            informatieobjecttypetrefwoord=['abc', 'def']
        )

        self.informatieobjecttype_list_url = get_operation_url(
            'informatieobjecttype_list',
            catalogus_uuid=self.catalogus.uuid
        )
        self.informatieobjecttype_detail_url = get_operation_url(
            'informatieobjecttype_read',
            catalogus_uuid=self.catalogus.uuid,
            uuid=self.informatieobjecttype.uuid
        )

    def test_get_list(self):
        """Retrieve a list of `InformatieObjectType` objects."""
        response = self.api_client.get(self.informatieobjecttype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `InformatieObjectType` object."""
        response = self.api_client.get(self.informatieobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            # 'categorie': 'informatieobjectcategorie',
            # 'einddatumObject': None,
            # 'ingangsdatumObject': '2018-01-01',
            # 'isVastleggingVoor': [],
            'catalogus': 'http://testserver{}'.format(self.catalogus_detail_url),
            # 'model': ['http://www.example.com'],
            'omschrijving': self.informatieobjecttype.informatieobjecttype_omschrijving,
            # 'omschrijvingGeneriek': '',
            # 'toelichting': None,
            # 'trefwoord': ['abc', 'def'],
            'url': 'http://testserver{}'.format(self.informatieobjecttype_detail_url),
            # 'vertrouwelijkAanduiding': None,
            # 'isRelevantVoor': [],
        }
        self.assertEqual(expected, response.json())

    @skip("Not MVP yet")
    def test_is_relevant_voor(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)

        ziot = ZaakInformatieobjectTypeFactory.create(
            zaaktype=zaaktype,
            informatie_object_type=self.informatieobjecttype,
            volgnummer=1,
            richting='richting',
        )

        response = self.api_client.get(self.informatieobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('isRelevantVoor' in data)
        self.assertEqual(len(data['isRelevantVoor']), 1)
        self.assertEqual(
            data['isRelevantVoor'][0],
            'http://testserver{}'.format(reverse('api:zktiot-detail', args=[
                self.API_VERSION, self.catalogus.pk, zaaktype.pk, ziot.pk
            ]))
        )

    @skip("Not MVP yet")
    def test_is_vastlegging_voor(self):
        pass
