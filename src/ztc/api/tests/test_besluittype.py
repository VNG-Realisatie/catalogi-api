from unittest import skip

from django.urls import reverse

from ...datamodel.tests.factories import BesluitTypeFactory
from .base import APITestCase


@skip("Not MVP yet")
class BesluitTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.besluittype = BesluitTypeFactory.create(
            maakt_deel_uit_van=self.catalogus,
            publicatie_indicatie='J'
        )

        self.is_relevant_voor = self.besluittype.zaaktypes.get()
        self.is_resultaat_van = self.besluittype.is_resultaat_van.get()

        self.besluittype_list_url = reverse('api:besluittype-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
        })

        self.besluittype_detail_url = reverse('api:besluittype-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'pk': self.besluittype.pk
        })

    def test_get_list(self):
        """Retrieve a list of `BesluitType` objects."""
        response = self.api_client.get(self.besluittype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        """Retrieve the details of a single `BesluitType` object."""
        response = self.api_client.get(self.besluittype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'einddatumObject': None,
            'ingangsdatumObject': '2018-01-01',
            'isRelevantVoor': [
                'http://testserver{}'.format(
                    reverse('api:zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.is_relevant_voor.pk])
                )
            ],
            'isResultaatVan': [
                'http://testserver{}'.format(
                    reverse('api:resultaattype-detail', args=[
                        self.API_VERSION, self.catalogus.pk,
                        self.is_resultaat_van.is_relevant_voor.pk, self.is_resultaat_van.pk
                    ])
                )
            ],
            'categorie': None,
            'maaktDeeluitVan': 'http://testserver{}'.format(self.catalogus_detail_url),
            'omschrijving': 'Besluittype',
            'omschrijvingGeneriek': None,
            'publicatieIndicatie': 'J',
            'publicatieTekst': None,
            'publicatieTermijn': None,
            'reactietermijn': 14,
            'toelichting': None,
            'url': 'http://testserver{}'.format(self.besluittype_detail_url),
            'wordtVastgelegdIn': []
        }
        self.assertEqual(response.json(), expected)

    def test_wordt_vastgelegd_in(self):
        pass
