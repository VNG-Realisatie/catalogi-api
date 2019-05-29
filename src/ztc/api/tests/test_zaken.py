import uuid
from unittest import skip

from django.urls import reverse

from rest_framework import status
from vng_api_common.tests import get_operation_url

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
            'identificatie': self.zaaktype.zaaktype_identificatie,
            'productenOfDiensten': ['https://example.com/product/123'],
            # 'broncatalogus': None,
            'publicatieIndicatie': self.zaaktype.publicatie_indicatie,
            'trefwoorden': [],
            # 'zaakcategorie': None,
            'toelichting': '',
            'handelingInitiator': self.zaaktype.handeling_initiator,
            # 'bronzaaktype': None,
            'aanleiding': self.zaaktype.aanleiding,
            'verlengingstermijn': None if not self.zaaktype.verlenging_mogelijk else 'P30D',
            'opschortingEnAanhoudingMogelijk': self.zaaktype.opschorting_en_aanhouding_mogelijk,
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'indicatieInternOfExtern': self.zaaktype.indicatie_intern_of_extern,
            'verlengingMogelijk': self.zaaktype.verlenging_mogelijk,
            'handelingBehandelaar': self.zaaktype.handeling_behandelaar,
            'doel': self.zaaktype.doel,
            # 'versiedatum': '2018-01-01',
            # 'formulier': [],
            'onderwerp': self.zaaktype.onderwerp,
            'publicatietekst': '',
            'omschrijvingGeneriek': '',
            'vertrouwelijkheidaanduiding': '',
            'verantwoordingsrelatie': [],
            'selectielijstProcestype': self.zaaktype.selectielijst_procestype,
            # 'isDeelzaaktypeVan': [],
            'servicenorm': None,
            # 'archiefclassificatiecode': None,
            'referentieproces': {
                'naam': self.zaaktype.referentieproces_naam,
                'link': '',
            },
            'doorlooptijd': "P30D",
            # 'verantwoordelijke': '',
            'omschrijving': '',
            'eigenschappen': [],
            'informatieobjecttypen': [],
            'gerelateerdeZaaktypen': [],
            # 'heeftRelevantBesluittype': [],
            # 'heeftRelevantZaakObjecttype': [],
            'statustypen': [],
            'resultaattypen': [],
            'roltypen': [],
            'besluittypen': [],
        }
        self.assertEqual(expected, response.json())

    def test_get_detail_404(self):
        url = get_operation_url(
            'zaaktype_read',
            catalogus_uuid=uuid.uuid4(),
            uuid=uuid.uuid4()
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        resp_data = response.json()
        del resp_data['instance']
        self.assertEqual(resp_data, {
            'code': 'not_found',
            'title': "Niet gevonden.",
            'status': 404,
            'detail': "Niet gevonden.",
            'type': "http://testserver{}".format(
                reverse('vng_api_common:error-detail', kwargs={'exception_class': 'NotFound'})
            )
        })

    @skip('Not implemented yet')
    def test_formulier(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_relevant_informatieobjecttype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_relevant_resultaattype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_relevant_besluittype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_relevant_zaakobjecttype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_eigenschap(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_roltype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_statustype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_heeft_gerelateerd(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_is_deelzaaktype_van(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_verantwoordingsrelatie(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_bronzaaktype(self):
        raise NotImplementedError()

    @skip('Not implemented yet')
    def test_broncatalogus(self):
        raise NotImplementedError()


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
