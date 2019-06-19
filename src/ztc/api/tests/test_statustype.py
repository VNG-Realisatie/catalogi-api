from rest_framework import status
from .utils import reverse

from ztc.datamodel.tests.factories import StatusTypeFactory, ZaakTypeFactory
from ztc.datamodel.models import StatusType

from .base import APITestCase


class StatusTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        StatusTypeFactory.create(
            statustype_omschrijving='Besluit genomen',
            zaaktype__catalogus=self.catalogus,
        )
        statustype_list_url = reverse('statustype-list')

        response = self.api_client.get(statustype_list_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        status_type = StatusTypeFactory.create(
            statustype_omschrijving='Besluit genomen',
            zaaktype__catalogus=self.catalogus,
            datum_begin_geldigheid='2019-01-01'
        )
        statustype_detail_url = reverse('statustype-detail', kwargs={
            'uuid': status_type.uuid,
        })
        zaaktype = status_type.zaaktype
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })

        response = self.api_client.get(statustype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver{}'.format(statustype_detail_url),
            'omschrijving': 'Besluit genomen',
            'omschrijvingGeneriek': '',
            'statustekst': '',
            'zaaktype': 'http://testserver{}'.format(zaaktype_url),
            'volgnummer': status_type.statustypevolgnummer,
            'isEindstatus': True,
            'datumBeginGeldigheid': '2019-01-01'
        }

        self.assertEqual(expected, response.json())

    def test_create_statustype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        statustype_list_url = reverse('statustype-list')
        data = {
            'omschrijving': 'Besluit genomen',
            'omschrijvingGeneriek': '',
            'statustekst': '',
            'zaaktype': 'http://testserver{}'.format(zaaktype_url),
            'volgnummer': 2,
            'datumBeginGeldigheid': '2019-01-01'
        }
        response = self.client.post(statustype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        statustype = StatusType.objects.get()

        self.assertEqual(statustype.statustype_omschrijving, 'Besluit genomen')
