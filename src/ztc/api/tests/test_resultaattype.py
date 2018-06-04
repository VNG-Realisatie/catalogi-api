from unittest import skip

from django.urls import reverse

from ztc.datamodel.tests.factories import ResultaatTypeFactory

from .base import APITestCase


@skip("Not MVP yet")
class ResultaatTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.resultaattype = ResultaatTypeFactory.create(
            resultaattypeomschrijving='Verleend',
            is_relevant_voor__maakt_deel_uit_van=self.catalogus,
            bepaalt_afwijkend_archiefregime_van=None,
        )
        self.zaaktype = self.resultaattype.is_relevant_voor

        self.resultaattype_list_url = reverse('api:resultaattype-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.resultaattype_detail_url = reverse('api:resultaattype-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.resultaattype.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.resultaattype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.resultaattype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'archiefactietermijn': 14,
            'archiefnominatie': '',
            'bepaaltAfwijkendArchiefRegimeVan': [],
            'brondatumProcedure': 'eigenschap',
            'einddatumObject': None,
            'heeftVerplichtDocumentype': [],
            'heeftVerplichteZaakobjecttype': [],
            'heeftVoorBrondatumArchiefprocedureRelevante': None,
            'ingangsdatumObject': '2018-01-01',
            'isRelevantVoor': 'http://testserver{}'.format(
                reverse('api:zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk])),
            'leidtTot': [],
            'omschrijving': 'Verleend',
            'omschrijvingGeneriek': '',
            'selectielijstklasse': None,
            'toelichting': None,
            'url': 'http://testserver{}'.format(self.resultaattype_detail_url)
        }
        self.assertEqual(expected, response.json())

    def test_bepaalt_afwijkend_archiefregime_van(self):
        pass

    def test_heeft_verplichte_zaakobjecttype(self):
        pass

    def test_heeft_verplicht_documenttype(self):
        pass

    def test_heeft_voor_brondatum_archiefprocedure_revelante(self):
        pass

    def test_leidt_tot(self):
        pass
