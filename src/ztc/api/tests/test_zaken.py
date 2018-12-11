from unittest import skip

from django.urls import reverse

from zds_schema.tests import get_operation_url

from ztc.datamodel.tests.factories import (
    ZaakObjectTypeFactory, ZaakTypeFactory
)

from .base import APITestCase


class ZaakTypeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)

        self.zaaktype_list_url = get_operation_url(
            'zaaktype_list',
            catalogus_uuid=self.catalogus.uuid
        )
        self.zaaktype_detail_url = get_operation_url(
            'zaaktype_read',
            catalogus_uuid=self.catalogus.uuid,
            uuid=self.zaaktype.uuid
        )

    def test_get_list(self):
        response = self.api_client.get(self.zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.zaaktype_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': f'http://testserver{self.zaaktype_detail_url}',
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
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            # 'indicatieInternOfExtern': '',
            # 'verlengingmogelijk': '',
            # 'handelingBehandelaar': '',
            # 'doel': '',
            # 'versiedatum': '2018-01-01',
            # 'formulier': [],
            # 'onderwerp': '',
            # 'publicatietekst': None,
            'omschrijvingGeneriek': '',
            # 'verantwoordingsrelatie': [],
            # 'isDeelzaaktypeVan': [],
            'servicenorm': None,
            # 'archiefclassificatiecode': None,
            # 'referentieproces': {
            #     'link': None,
            #     'naam': self.zaaktype.referentieproces.naam,
            # },
            'doorlooptijd': "P30D",
            # 'verantwoordelijke': '',
            'omschrijving': '',
            # 'heeftGerelateerd': [],
            # 'heeftRelevantInformatieobjecttype': [],
            'eigenschappen': [],
            # 'heeftRelevantBesluittype': [],
            # 'heeftRelevantResultaattype': [],
            # 'heeftRelevantZaakObjecttype': [],
            'statustypen': [],
            'roltypen': [],
            'besluittypen': [],
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

        self.zaakobjecttype = ZaakObjectTypeFactory.create(is_relevant_voor__catalogus=self.catalogus)

        self.zaaktype = self.zaakobjecttype.is_relevant_voor

        self.zaakobjecttype_list_url = reverse('zaakobjecttype-list', kwargs={
            'version': self.API_VERSION,
            'zaaktype_uuid': self.zaaktype.uuid,
            'catalogus_uuid': self.catalogus.uuid,
        })
        self.zaakobjecttype_detail_url = reverse('zaakobjecttype-detail', kwargs={
            'version': self.API_VERSION,
            'zaaktype_uuid': self.zaaktype.uuid,
            'catalogus_uuid': self.catalogus.uuid,
            'uuid': self.zaakobjecttype.uuid,
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
                reverse('zaaktype-detail', args=[self.API_VERSION, self.catalogus.pk, self.zaaktype.pk])),
            'objecttype': '',
            'relatieOmschrijving': '',
            'url': 'http://testserver{}'.format(self.zaakobjecttype_detail_url)
        }
        self.assertEqual(expected, response.json())
