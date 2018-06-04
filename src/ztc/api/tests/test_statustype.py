from unittest import skip

from django.urls import reverse

from ztc.datamodel.tests.factories import StatusTypeFactory

from .base import APITestCase


@skip("Not MVP yet")
class StatusTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.status_type = StatusTypeFactory.create(
            statustype_omschrijving='Besluit genomen',
            is_van__maakt_deel_uit_van=self.catalogus,
        )

        self.zaaktype = self.status_type.is_van

        self.statustype_list_url = reverse('api:statustype-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.statustype_detail_url = reverse('api:statustype-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.status_type.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.statustype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.statustype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'doorlooptijd': None,
            'informeren': '',
            'toelichting': None,
            'omschrijving': 'Besluit genomen',
            'volgnummer': self.status_type.statustypevolgnummer,
            'checklistitem': [],
            'ingangsdatumObject': '2018-01-01',
            'einddatumObject': None,
            'heeftVerplichteEigenschap': [],
            'heeftVerplichteZaakObjecttype': [],
            'url': 'http://testserver{}'.format(self.statustype_detail_url),
            'statustekst': None,
            'isVan': 'http://testserver{}'.format(
                reverse('api:zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk])),
            'omschrijvingGeneriek': None,
            'heeftVerplichteInformatieobjecttype': [],
        }
        self.assertEqual(expected, response.json())

    def test_checklistitem(self):
        pass

    def test_heeft_verplichte_eigenschap(self):
        pass

    def test_heeft_verplichte_zaakobjecttype(self):
        pass

    def test_heeft_verplichte_informatieobjecttype(self):
        pass
