from ...datamodel.tests.factories import BesluitTypeFactory
from .base import APITestCase
from .utils import reverse


class BesluitTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.besluittype = BesluitTypeFactory.create(
            catalogus=self.catalogus,
            publicatie_indicatie=True
        )
        self.zaaktype = self.besluittype.zaaktypes.get()
        self.resultaattype = self.besluittype.resultaattypes.get()

        self.besluittype_list_url = reverse('besluittype-list', kwargs={
            'catalogus_uuid': self.catalogus.uuid,
        })

        self.besluittype_detail_url = reverse('besluittype-detail', kwargs={
            'catalogus_uuid': self.catalogus.uuid,
            'uuid': self.besluittype.uuid
        })

    def test_get_list(self):
        """Retrieve a list of `BesluitType` objects."""
        response = self.client.get(self.besluittype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # pagination disabled for now
        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `BesluitType` object."""
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'catalogus_uuid': self.catalogus.uuid,
            'uuid': self.zaaktype.uuid,
        })
        # resultaattype_url = reverse('resultaattype-detail', kwargs={
        #     'catalogus_uuid': self.catalogus.uuid,
        #     'zaaktype_uuid': self.zaaktype.uuid,
        #     'uuid': self.resultaattype.uuid,
        # })

        response = self.client.get(self.besluittype_detail_url)

        self.assertEqual(response.status_code, 200)
        expected = {
            'url': f'http://testserver{self.besluittype_detail_url}',
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
            # 'resultaattypes': ['http://testserver{resultaattype_url}'],
            # 'einddatumObject': None,
            # 'ingangsdatumObject': '2018-01-01',
        }
        self.assertEqual(response.json(), expected)
