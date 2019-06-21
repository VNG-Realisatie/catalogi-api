from rest_framework import status

from ...datamodel.tests.factories import BesluitTypeFactory, ZaakTypeFactory, InformatieObjectTypeFactory
from ...datamodel.models import BesluitType
from .base import APITestCase
from .utils import reverse


class BesluitTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list(self):
        """Retrieve a list of `BesluitType` objects."""
        BesluitTypeFactory.create(
            catalogus=self.catalogus,
            publicatie_indicatie=True
        )
        besluittype_list_url = reverse('besluittype-list')

        response = self.client.get(besluittype_list_url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        # pagination disabled for now
        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `BesluitType` object."""
        besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus,
            publicatie_indicatie=True,
        )
        zaaktype = besluittype.zaaktypes.get()
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        besluittype_detail_url = reverse('besluittype-detail', kwargs={
            'uuid': besluittype.uuid
        })

        # resultaattype_url = reverse('resultaattype-detail', kwargs={
        #     'catalogus_uuid': self.catalogus.uuid,
        #     'zaaktype_uuid': self.zaaktype.uuid,
        #     'uuid': self.resultaattype.uuid,
        # })

        response = self.client.get(besluittype_detail_url)

        self.assertEqual(response.status_code, 200)
        expected = {
            'url': f'http://testserver{besluittype_detail_url}',
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'zaaktypes': [f'http://testserver{zaaktype_url}'],
            'omschrijving': 'Besluittype',
            'omschrijvingGeneriek': '',
            'besluitcategorie': '',
            'reactietermijn': 'P14D',
            'publicatieIndicatie': True,
            'publicatietekst': '',
            'publicatietermijn': None,
            'toelichting': '',
            'informatieobjecttypes': [],
            'beginGeldigheid': '2018-01-01',
            'eindeGeldigheid': None,
            'draft': True,
            # 'resultaattypes': ['http://testserver{resultaattype_url}'],
        }
        self.assertEqual(response.json(), expected)

    def test_create_besluittype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse('informatieobjecttype-detail', kwargs={
            'uuid': informatieobjecttype.uuid,
        })
        besluittype_list_url = reverse('besluittype-list')
        data = {
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'zaaktypes': [f'http://testserver{zaaktype_url}'],
            'omschrijving': 'test',
            'omschrijvingGeneriek': '',
            'besluitcategorie': '',
            'reactietermijn': 'P14D',
            'publicatieIndicatie': True,
            'publicatietekst': '',
            'publicatietermijn': None,
            'toelichting': '',
            'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            'beginGeldigheid': '2019-01-01',
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        besluittype = BesluitType.objects.get()

        self.assertEqual(besluittype.omschrijving, 'test')
        self.assertEqual(besluittype.catalogus, self.catalogus)
        self.assertEqual(besluittype.zaaktypes.get(), zaaktype)
        self.assertEqual(besluittype.informatieobjecttypes.get(), informatieobjecttype)
        self.assertEqual(besluittype.draft, True)

    def test_create_besluittype_fail_non_draft_zaaktypes(self):
        zaaktype = ZaakTypeFactory.create(draft=False)
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse('informatieobjecttype-detail', kwargs={
            'uuid': informatieobjecttype.uuid,
        })
        besluittype_list_url = reverse('besluittype-list')
        data = {
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'zaaktypes': [f'http://testserver{zaaktype_url}'],
            'omschrijving': 'test',
            'omschrijvingGeneriek': '',
            'besluitcategorie': '',
            'reactietermijn': 'P14D',
            'publicatieIndicatie': True,
            'publicatietekst': '',
            'publicatietermijn': None,
            'toelichting': '',
            'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            'beginGeldigheid': '2019-01-01',
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], "Relations to a non-draft object can't be created")

    def test_create_besluittype_fail_non_draft_informatieobjecttypes(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        informatieobjecttype = InformatieObjectTypeFactory.create(draft=False)
        informatieobjecttype_url = reverse('informatieobjecttype-detail', kwargs={
            'uuid': informatieobjecttype.uuid,
        })
        besluittype_list_url = reverse('besluittype-list')
        data = {
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'zaaktypes': [f'http://testserver{zaaktype_url}'],
            'omschrijving': 'test',
            'omschrijvingGeneriek': '',
            'besluitcategorie': '',
            'reactietermijn': 'P14D',
            'publicatieIndicatie': True,
            'publicatietekst': '',
            'publicatietermijn': None,
            'toelichting': '',
            'informatieobjecttypes': [f'http://testserver{informatieobjecttype_url}'],
            'beginGeldigheid': '2019-01-01',
        }

        response = self.client.post(besluittype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], "Relations to a non-draft object can't be created")

    def test_publish_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse('besluittype-publish', kwargs={
            'uuid': besluittype.uuid,
        })

        response = self.client.post(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        besluittype.refresh_from_db()

        self.assertEqual(besluittype.draft, False)

    def test_delete_besluittype(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = reverse('besluittype-detail', kwargs={
            'uuid': besluittype.uuid,
        })

        response = self.client.delete(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BesluitType.objects.exists())

    def test_delete_besluittype_fail_not_draft(self):
        besluittype = BesluitTypeFactory.create(draft=False)
        besluittype_url = reverse('besluittype-detail', kwargs={
            'uuid': besluittype.uuid,
        })

        response = self.client.delete(besluittype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-draft object is forbidden')
