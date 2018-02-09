from django.urls import reverse

from ...datamodel.tests.factories import InformatieObjectTypeFactory
from .base import APITestCase


class InformatieObjectTypeAPITests(APITestCase):
    def setUp(self):
        super().setUp()

        self.informatieobjecttype = InformatieObjectTypeFactory.create(maakt_deel_uit_van=self.catalogus)

        self.informatieobjecttype_list_url = reverse('api:informatieobjecttype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
        })

        self.informatieobjecttype_detail_url = reverse('api:informatieobjecttype-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'pk': self.informatieobjecttype.pk
        })

    def test_get_list(self):
        """Retrieve a list of `InformatieObjectType` objects."""
        response = self.api_client.get(self.informatieobjecttype_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/'.format(
                        self.catalogus.pk)
                }
            },
            'results': [
                {
                    'trefwoord': [],
                    'einddatumObject': None,
                    'maaktDeeluitVan': 'http://testserver/api/v1/catalogussen/{}/'.format(
                        self.catalogus.pk),
                    'omschrijvingGeneriek': '',
                    'categorie': 'informatieobjectcategorie',
                    'vertrouwelijkAanduiding': None,
                    'isVastleggingVoor': [],
                    'model': [],
                    'toelichting': None,
                    'omschrijving': self.informatieobjecttype.informatieobjecttype_omschrijving,
                    'ingangsdatumObject': '',
                    'url': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/'.format(
                        self.catalogus.pk, self.informatieobjecttype.pk)
                }
            ]
        }
        self.assertEqual(expected, response.json())

    def test_get_detail(self):
        """Retrieve the details of a single `InformatieObjectType` object."""
        response = self.api_client.get(self.informatieobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'categorie': 'informatieobjectcategorie',
            'einddatumObject': None,
            'ingangsdatumObject': '',
            'isVastleggingVoor': [],
            'maaktDeeluitVan': 'http://testserver/api/v1/catalogussen/{}/'.format(
                self.catalogus.pk),
            'model': [],
            'omschrijving': self.informatieobjecttype.informatieobjecttype_omschrijving,
            'omschrijvingGeneriek': '',
            'toelichting': None,
            'trefwoord': [],
            'url': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/'.format(
                self.catalogus.pk, self.informatieobjecttype.pk),
            'vertrouwelijkAanduiding': None
        }
        self.assertEqual(expected, response.json())
