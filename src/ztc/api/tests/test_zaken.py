import uuid
from unittest import skip

from django.urls import reverse

from rest_framework import status
from vng_api_common.constants import VertrouwelijkheidsAanduiding
from vng_api_common.tests import get_operation_url, get_validation_errors

from ztc.datamodel.choices import AardRelatieChoices, InternExtern
from ztc.datamodel.models import ZaakType
from ztc.datamodel.tests.factories import (
    BesluitTypeFactory, ZaakObjectTypeFactory, ZaakTypeFactory
)

from .base import APITestCase


class ZaakTypeAPITests(APITestCase):
    maxDiff = None

    def test_get_list_default_nondraft(self):
        zaaktype1 = ZaakTypeFactory.create(draft=True)
        zaaktype2 = ZaakTypeFactory.create(draft=False)
        zaaktype_list_url = get_operation_url('zaaktype_list')
        zaaktype2_url = get_operation_url('zaaktype_read', uuid=zaaktype2.uuid)

        response = self.client.get(zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{zaaktype2_url}')

    def test_get_detail(self):
        zaaktype = ZaakTypeFactory.create(catalogus=self.catalogus)
        zaaktype_detail_url = get_operation_url('zaaktype_read', uuid=zaaktype.uuid)

        response = self.api_client.get(zaaktype_detail_url)

        self.assertEqual(response.status_code, 200)

        expected = {
            'url': f'http://testserver{zaaktype_detail_url}',
            # 'ingangsdatumObject': '2018-01-01',
            # 'einddatumObject': None,
            'identificatie': zaaktype.zaaktype_identificatie,
            'productenOfDiensten': ['https://example.com/product/123'],
            # 'broncatalogus': None,
            'publicatieIndicatie': zaaktype.publicatie_indicatie,
            'trefwoorden': [],
            # 'zaakcategorie': None,
            'toelichting': '',
            'handelingInitiator': zaaktype.handeling_initiator,
            # 'bronzaaktype': None,
            'aanleiding': zaaktype.aanleiding,
            'verlengingstermijn': None if not zaaktype.verlenging_mogelijk else 'P30D',
            'opschortingEnAanhoudingMogelijk': zaaktype.opschorting_en_aanhouding_mogelijk,
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            'indicatieInternOfExtern': zaaktype.indicatie_intern_of_extern,
            'verlengingMogelijk': zaaktype.verlenging_mogelijk,
            'handelingBehandelaar': zaaktype.handeling_behandelaar,
            'doel': zaaktype.doel,
            # 'versiedatum': '2018-01-01',
            # 'formulier': [],
            'onderwerp': zaaktype.onderwerp,
            'publicatietekst': '',
            'omschrijvingGeneriek': '',
            'vertrouwelijkheidaanduiding': '',
            'verantwoordingsrelatie': [],
            'selectielijstProcestype': zaaktype.selectielijst_procestype,
            # 'isDeelzaaktypeVan': [],
            'servicenorm': None,
            # 'archiefclassificatiecode': None,
            'referentieproces': {
                'naam': zaaktype.referentieproces_naam,
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
            'beginGeldigheid': '2018-01-01',
            'eindeGeldigheid': None,
            'versiedatum': '2018-01-01',
            'draft': True,
        }
        self.assertEqual(expected, response.json())

    def test_get_detail_404(self):
        ZaakTypeFactory.create(catalogus=self.catalogus)

        url = get_operation_url('zaaktype_read', uuid=uuid.uuid4())

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

    def test_create_zaaktype(self):
        besluittype = BesluitTypeFactory.create(catalogus=self.catalogus)
        besluittype_url = get_operation_url('besluittype_read', uuid=besluittype.uuid)

        zaaktype_list_url = get_operation_url('zaaktype_list')
        data = {
            'identificatie': 0,
            'doel': 'some test',
            'aanleiding': 'some test',
            'indicatieInternOfExtern': InternExtern.extern,
            'handelingInitiator': 'indienen',
            'onderwerp': 'Klacht',
            'handelingBehandelaar': 'uitvoeren',
            'doorlooptijd': 'P30D',
            'opschortingEnAanhoudingMogelijk': False,
            'verlengingMogelijk': True,
            'verlengingstermijn': 'P30D',
            'publicatieIndicatie': True,
            'verantwoordingsrelatie': [],
            'productenOfDiensten': ['https://example.com/product/123'],
            'vertrouwelijkheidaanduiding': VertrouwelijkheidsAanduiding.openbaar,
            'omschrijving': 'some test',
            'gerelateerdeZaaktypen': [
                {
                    'zaaktype': 'http://example.com/zaaktype/1',
                    'aard_relatie': AardRelatieChoices.bijdrage,
                    'toelichting': 'test relations'
                },
            ],
            'referentieproces': {
                'naam': 'ReferentieProces 0',
                'link': ''
            },
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            # 'informatieobjecttypen': [f'http://testserver{informatieobjecttype_url}'],
            'besluittypen': [f'http://testserver{besluittype_url}'],
            'beginGeldigheid': '2018-01-01',
            'versiedatum': '2018-01-01',
        }
        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        zaaktype = ZaakType.objects.get(zaaktype_omschrijving='some test')

        self.assertEqual(zaaktype.catalogus, self.catalogus)
        self.assertEqual(zaaktype.besluittype_set.get(), besluittype)
        self.assertEqual(zaaktype.referentieproces_naam, 'ReferentieProces 0')
        self.assertEqual(zaaktype.zaaktypenrelaties.get().gerelateerd_zaaktype, 'http://example.com/zaaktype/1')
        self.assertEqual(zaaktype.draft, True)

    def test_create_zaaktype_fail_besluittype_non_draft(self):
        besluittype = BesluitTypeFactory.create(draft=False, catalogus=self.catalogus)
        besluittype_url = get_operation_url('besluittype_read', uuid=besluittype.uuid)

        zaaktype_list_url = get_operation_url('zaaktype_list')
        data = {
            'identificatie': 0,
            'doel': 'some test',
            'aanleiding': 'some test',
            'indicatieInternOfExtern': InternExtern.extern,
            'handelingInitiator': 'indienen',
            'onderwerp': 'Klacht',
            'handelingBehandelaar': 'uitvoeren',
            'doorlooptijd': 'P30D',
            'opschortingEnAanhoudingMogelijk': False,
            'verlengingMogelijk': True,
            'verlengingstermijn': 'P30D',
            'publicatieIndicatie': True,
            'verantwoordingsrelatie': [],
            'productenOfDiensten': ['https://example.com/product/123'],
            'vertrouwelijkheidaanduiding': VertrouwelijkheidsAanduiding.openbaar,
            'omschrijving': 'some test',
            'gerelateerdeZaaktypen': [
                {
                    'zaaktype': 'http://example.com/zaaktype/1',
                    'aard_relatie': AardRelatieChoices.bijdrage,
                    'toelichting': 'test relations'
                },
            ],
            'referentieproces': {
                'naam': 'ReferentieProces 0',
                'link': ''
            },
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            # 'informatieobjecttypen': [f'http://testserver{informatieobjecttype_url}'],
            'besluittypen': [f'http://testserver{besluittype_url}'],
            'beginGeldigheid': '2018-01-01',
            'versiedatum': '2018-01-01',
        }

        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], "Relations to a non-draft besluittype_set object can't be created")

    def test_create_zaaktype_fail_different_catalogus_besluittypes(self):
        besluittype = BesluitTypeFactory.create()
        besluittype_url = get_operation_url('besluittype_read', uuid=besluittype.uuid)

        zaaktype_list_url = get_operation_url('zaaktype_list')
        data = {
            'identificatie': 0,
            'doel': 'some test',
            'aanleiding': 'some test',
            'indicatieInternOfExtern': InternExtern.extern,
            'handelingInitiator': 'indienen',
            'onderwerp': 'Klacht',
            'handelingBehandelaar': 'uitvoeren',
            'doorlooptijd': 'P30D',
            'opschortingEnAanhoudingMogelijk': False,
            'verlengingMogelijk': True,
            'verlengingstermijn': 'P30D',
            'publicatieIndicatie': True,
            'verantwoordingsrelatie': [],
            'productenOfDiensten': ['https://example.com/product/123'],
            'vertrouwelijkheidaanduiding': VertrouwelijkheidsAanduiding.openbaar,
            'omschrijving': 'some test',
            'gerelateerdeZaaktypen': [
                {
                    'zaaktype': 'http://example.com/zaaktype/1',
                    'aard_relatie': AardRelatieChoices.bijdrage,
                    'toelichting': 'test relations'
                },
            ],
            'referentieproces': {
                'naam': 'ReferentieProces 0',
                'link': ''
            },
            'catalogus': f'http://testserver{self.catalogus_detail_url}',
            # 'informatieobjecttypen': [f'http://testserver{informatieobjecttype_url}'],
            'besluittypen': [f'http://testserver{besluittype_url}'],
            'beginGeldigheid': '2018-01-01',
            'versiedatum': '2018-01-01',
        }
        response = self.client.post(zaaktype_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

        error = get_validation_errors(response, 'nonFieldErrors')
        self.assertEqual(error['code'], 'relations-incorrect-catalogus')

    def test_publish_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = get_operation_url('zaaktype_publish', uuid=zaaktype.uuid)

        response = self.client.post(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        zaaktype.refresh_from_db()

        self.assertEqual(zaaktype.draft, False)

    def test_delete_zaaktype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = get_operation_url('zaaktype_read', uuid=zaaktype.uuid)

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakType.objects.filter(id=zaaktype.id))

    def test_delete_zaaktype_fail_not_draft(self):
        zaaktype = ZaakTypeFactory.create(draft=False)
        zaaktype_url = get_operation_url('zaaktype_read', uuid=zaaktype.uuid)

        response = self.client.delete(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-draft object is forbidden')


class ZaakTypeFilterAPITests(APITestCase):
    maxDiff = None

    def test_filter_zaaktype_publish_all(self):
        ZaakTypeFactory.create(draft=True)
        ZaakTypeFactory.create(draft=False)
        zaaktype_list_url = get_operation_url('zaaktype_list')

        response = self.client.get(zaaktype_list_url, {'publish': 'all'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 2)

    def test_filter_zaaktype_publish_draft(self):
        zaaktype1 = ZaakTypeFactory.create(draft=True)
        zaaktype2 = ZaakTypeFactory.create(draft=False)
        zaaktype_list_url = get_operation_url('zaaktype_list')
        zaaktype1_url = get_operation_url('zaaktype_read', uuid=zaaktype1.uuid)

        response = self.client.get(zaaktype_list_url, {'publish': 'draft'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{zaaktype1_url}')

    def test_filter_zaaktype_publish_nondraft(self):
        zaaktype1 = ZaakTypeFactory.create(draft=True)
        zaaktype2 = ZaakTypeFactory.create(draft=False)
        zaaktype_list_url = get_operation_url('zaaktype_list')
        zaaktype2_url = get_operation_url('zaaktype_read', uuid=zaaktype2.uuid)

        response = self.client.get(zaaktype_list_url, {'publish': 'nondraft'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{zaaktype2_url}')


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
