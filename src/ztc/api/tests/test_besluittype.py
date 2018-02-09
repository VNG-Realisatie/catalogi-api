from django.urls import reverse

from ...datamodel.tests.factories import BesluitTypeFactory
from .base import APITestCase


class BesluitTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.besluittype = BesluitTypeFactory.create(
            maakt_deel_uit_van=self.catalogus, publicatie_indicatie='J')

        self.besluittype_list_url = reverse('api:besluittype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
        })

        self.besluittype_detail_url = reverse('api:besluittype-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'pk': self.besluittype.pk
        })

    def test_get_list(self):
        """Retrieve a list of `BesluitType` objects."""
        response = self.api_client.get(self.besluittype_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/besluittypen/'.format(
                        self.catalogus.pk)
                }
            },
            'results': [
                {
                    'omschrijvingGeneriek': None,
                    'wordtVastgelegdIn': [],
                    'publicatieTermijn': None,
                    'publicatieIndicatie': 'J',
                    'url': 'http://testserver/api/v1/catalogussen/{}/besluittypen/{}/'.format(
                        self.catalogus.pk, self.besluittype.pk),
                    'omschrijving': 'Besluittype',
                    'publicatieTekst': None,
                    'categorie': None,
                    'toelichting': None,
                    'reactietermijn': 14,
                    'maaktDeeluitVan': 'http://testserver/api/v1/catalogussen/{}/'.format(
                        self.catalogus.pk)
                }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail(self):
        """Retrieve the details of a single `BesluitType` object."""
        response = self.api_client.get(self.besluittype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'categorie': None,
            'maaktDeeluitVan': 'http://testserver/api/v1/catalogussen/{}/'.format(
                self.catalogus.pk),
            'omschrijving': 'Besluittype',
            'omschrijvingGeneriek': None,
            'publicatieIndicatie': 'J',
            'publicatieTekst': None,
            'publicatieTermijn': None,
            'reactietermijn': 14,
            'toelichting': None,
            'url': 'http://testserver/api/v1/catalogussen/{}/besluittypen/{}/'.format(
                self.catalogus.pk, self.besluittype.pk),
            'wordtVastgelegdIn': []
        }
        self.assertEqual(response.json(), expected)
