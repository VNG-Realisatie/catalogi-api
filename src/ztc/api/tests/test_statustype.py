from rest_framework import status

from ztc.datamodel.models import StatusType
from ztc.datamodel.tests.factories import StatusTypeFactory, ZaakTypeFactory

from .base import APITestCase
from .utils import reverse


class StatusTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list_default_nonconcept(self):
        statustype1 = StatusTypeFactory.create(zaaktype__concept=True)
        statustype2 = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse('statustype-list')
        statustype2_url = reverse('statustype-detail', kwargs={'uuid': statustype2.uuid})

        response = self.client.get(statustype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{statustype2_url}')

    def test_get_detail(self):
        status_type = StatusTypeFactory.create(
            statustype_omschrijving='Besluit genomen',
            zaaktype__catalogus=self.catalogus,
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
        }
        response = self.client.post(statustype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        statustype = StatusType.objects.get()

        self.assertEqual(statustype.statustype_omschrijving, 'Besluit genomen')
        self.assertEqual(statustype.zaaktype, zaaktype)

    def test_create_statustype_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
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
        }
        response = self.client.post(statustype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Creating a related object to non-concept object is forbidden')

    def test_delete_statustype(self):
        statustype = StatusTypeFactory.create()
        statustype_url = reverse('statustype-detail', kwargs={'uuid': statustype.uuid})

        response = self.client.delete(statustype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(StatusType.objects.filter(id=statustype.id))

    def test_delete_statustype_fail_not_concept_zaaktype(self):
        statustype = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_url = reverse('statustype-detail', kwargs={'uuid': statustype.uuid})

        response = self.client.delete(statustype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-concept object is forbidden')


class StatusTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_statustype_publish_all(self):
        StatusTypeFactory.create(zaaktype__concept=True)
        StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse('statustype-list')

        response = self.client.get(statustype_list_url, {'publish': 'all'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 2)

    def test_filter_statustype_publish_concept(self):
        statustype1 = StatusTypeFactory.create(zaaktype__concept=True)
        statustype2 = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse('statustype-list')
        statustype1_url = reverse('statustype-detail', kwargs={'uuid': statustype1.uuid})

        response = self.client.get(statustype_list_url, {'publish': 'concept'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{statustype1_url}')

    def test_filter_statustype_publish_nonconcept(self):
        statustype1 = StatusTypeFactory.create(zaaktype__concept=True)
        statustype2 = StatusTypeFactory.create(zaaktype__concept=False)
        statustype_list_url = reverse('statustype-list')
        statustype2_url = reverse('statustype-detail', kwargs={'uuid': statustype2.uuid})

        response = self.client.get(statustype_list_url, {'publish': 'nonconcept'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{statustype2_url}')
