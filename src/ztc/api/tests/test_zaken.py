from unittest import skip

from django.urls import reverse

from ztc.datamodel.tests.factories import (
    ZaakObjectTypeFactory, ZaakTypeFactory
)

from .base import APITestCase


class ZaakTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.zaaktype = ZaakTypeFactory.create(maakt_deel_uit_van=self.catalogus)

        self.zaaktype_list_url = reverse('api:zaaktype-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
        })
        self.zaaktype_detail_url = reverse('api:zaaktype-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'pk': self.zaaktype.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.zaaktype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver{}'.format(self.zaaktype_detail_url),
            # 'ingangsdatumObject': '2018-01-01',
            # 'einddatumObject': None,
            # 'vertrouwelijkheidAanduiding': '',
            'identificatie': self.zaaktype.zaaktype_identificatie,
            # 'product_dienst': [{
            #     'naam': self.zaaktype.product_dienst.get().naam,
            #     'link': None
            # }],
            # 'broncatalogus': None,
            # 'publicatieIndicatie': '',
            # 'trefwoord': [],
            # 'zaakcategorie': None,
            # 'toelichting': None,
            # 'handelingInitiator': '',
            # 'bronzaaktype': None,
            # 'aanleiding': '',
            # 'verlengingstermijn': 30,
            # 'opschortingAanhouding': '',
            'maaktDeelUitVan': 'http://testserver{}'.format(self.catalogus_detail_url),
            # 'indicatieInternOfExtern': '',
            # 'verlengingmogelijk': '',
            # 'handelingBehandelaar': '',
            # 'doel': '',
            # 'versiedatum': '2018-01-01',
            # 'formulier': [],
            # 'onderwerp': '',
            # 'publicatietekst': None,
            'omschrijvingGeneriek': None,
            # 'verantwoordingsrelatie': [],
            # 'isDeelzaaktypeVan': [],
            # 'servicenorm': None,
            # 'archiefclassificatiecode': None,
            # 'referentieproces': {
            #     'link': None,
            #     'naam': self.zaaktype.referentieproces.naam,
            # },
            # 'doorlooptijd': 30,
            # 'verantwoordelijke': '',
            'omschrijving': '',
            # 'heeftGerelateerd': [],
            # 'heeftRelevantInformatieobjecttype': [],
            # 'heeftEigenschap': [],
            # 'heeftRelevantBesluittype': [],
            # 'heeftRelevantResultaattype': [],
            # 'heeftRelevantZaakObjecttype': [],
            # 'heeftRoltype': [],
            # 'heeftStatustype': [],
        }
        self.assertEqual(expected, response.json())

    def test_formulier(self):
        pass

    def test_heeft_relevant_informatieobjecttype(self):
        pass

    def test_heeft_relevant_resultaattype(self):
        pass

    def test_heeft_relevant_besluittype(self):
        pass

    def test_heeft_relevant_zaakobjecttype(self):
        pass

    def test_heeft_eigenschap(self):
        pass

    def test_heeft_roltype(self):
        pass

    def test_heeft_statustype(self):
        pass

    def test_heeft_gerelateerd(self):
        pass

    def test_is_deelzaaktype_van(self):
        pass

    def test_verantwoordingsrelatie(self):
        pass

    def test_bronzaaktype(self):
        pass

    def test_broncatalogus(self):
        pass


@skip("Not in current MVP")
class ZaakObjectTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.zaakobjecttype = ZaakObjectTypeFactory.create(is_relevant_voor__maakt_deel_uit_van=self.catalogus)

        self.zaaktype = self.zaakobjecttype.is_relevant_voor

        self.zaakobjecttype_list_url = reverse('api:zaakobjecttype-list', kwargs={
            'version': self.API_VERSION,
            'zaaktype_pk': self.zaaktype.pk,
            'catalogus_pk': self.catalogus.pk,
        })
        self.zaakobjecttype_detail_url = reverse('api:zaakobjecttype-detail', kwargs={
            'version': self.API_VERSION,
            'zaaktype_pk': self.zaaktype.pk,
            'catalogus_pk': self.catalogus.pk,
            'pk': self.zaakobjecttype.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.zaakobjecttype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.zaakobjecttype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'anderObject': '',
            'einddatumObject': None,
            'ingangsdatumObject': '2018-01-01',
            'isRelevantVoor': 'http://testserver{}'.format(
                reverse('api:zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk])),
            'objecttype': '',
            'relatieOmschrijving': '',
            'url': 'http://testserver{}'.format(self.zaakobjecttype_detail_url)
        }
        self.assertEqual(expected, response.json())
