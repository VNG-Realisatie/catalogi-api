from rest_framework import status
import requests_mock
from vng_api_common.tests import TypeCheckMixin, reverse, reverse_lazy
from vng_api_common.constants import BrondatumArchiefprocedureAfleidingswijze

from ztc.datamodel.models import ResultaatType
from ztc.datamodel.tests.factories import ResultaatTypeFactory, ZaakTypeFactory

from .base import APITestCase


class ResultaatTypeAPITests(TypeCheckMixin, APITestCase):
    maxDiff = None

    list_url = reverse_lazy(ResultaatType)

    def test_get_list(self):
        ResultaatTypeFactory.create_batch(3)

        response = self.api_client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 3)
        self.assertResponseTypes(
            data[0],
            (
                ('url', str),
                ('zaaktype', str),
                ('omschrijving', str),
                ('resultaattypeomschrijving', str),
                ('omschrijvingGeneriek', str),
                ('selectielijstklasse', str),
                ('toelichting', str),
                ('archiefnominatie', str),
                ('archiefactietermijn', str),
                ('brondatumArchiefprocedure', dict),
            )
        )

    def test_filter_on_zaaktype(self):
        zt1, zt2 = ZaakTypeFactory.create_batch(2)
        rt1 = ResultaatTypeFactory.create(zaaktype=zt1)
        rt1_url = f'http://testserver{reverse(rt1)}'
        rt2 = ResultaatTypeFactory.create(zaaktype=zt2)
        rt2_url = f'http://testserver{reverse(rt2)}'
        zt1_url = 'http://testserver{}'.format(reverse('zaaktype-detail', kwargs={
            'uuid': zt1.uuid,
        }))
        zt2_url = 'http://testserver{}'.format(reverse('zaaktype-detail', kwargs={
            'uuid': zt2.uuid,
        }))

        response = self.client.get(self.list_url, {'zaaktype': zt1_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['url'], rt1_url)
        self.assertEqual(response_data[0]['zaaktype'], zt1_url)
        self.assertNotEqual(response_data[0]['url'], rt2_url)
        self.assertNotEqual(response_data[0]['zaaktype'], zt2_url)

    def test_get_detail(self):
        resultaattype = ResultaatTypeFactory.create()
        url = reverse(resultaattype)
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': resultaattype.zaaktype.uuid,
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        self.assertEqual(response_data, {
            'url': f'http://testserver{url}',
            'zaaktype': f'http://testserver{zaaktype_url}',
            'omschrijving': resultaattype.omschrijving,
            'resultaattypeomschrijving': resultaattype.resultaattypeomschrijving,
            'omschrijvingGeneriek': resultaattype.omschrijving_generiek,
            'selectielijstklasse': resultaattype.selectielijstklasse,
            'toelichting': '',
            'archiefnominatie': resultaattype.archiefnominatie,
            'archiefactietermijn': 'P10Y',
            'brondatumArchiefprocedure': {
                'afleidingswijze': None,
                'datumkenmerk': None,
                'einddatumBekend': False,
                'objecttype': None,
                'registratie': None,
                'procestermijn': None,
            }
        })

    def test_resultaattypen_embedded_zaaktype(self):
        resultaattype = ResultaatTypeFactory.create()
        url = f'http://testserver{reverse(resultaattype)}'
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': resultaattype.zaaktype.uuid,
        })

        response = self.client.get(zaaktype_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['resultaattypen'],
            [url]
        )

    def test_resultaattype_afleidingswijze_procestermijn(self):
        resultaattype = ResultaatTypeFactory.create(
            brondatum_archiefprocedure_afleidingswijze='procestermijn',
            brondatum_archiefprocedure_procestermijn='P5Y',
        )

        url = reverse(resultaattype)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        brondatumArchiefprocedure = response.json()['brondatumArchiefprocedure']

        afleidingswijze = resultaattype.brondatum_archiefprocedure_afleidingswijze
        procestermijn = resultaattype.brondatum_archiefprocedure_procestermijn

        self.assertEqual(brondatumArchiefprocedure['afleidingswijze'], afleidingswijze)

        # Verify that the procestermijn was serialized correctly
        self.assertEqual(brondatumArchiefprocedure['procestermijn'], procestermijn)

    def test_create_resultaattype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse('zaaktype-detail', kwargs={
            'uuid': zaaktype.uuid,
        })
        resultaattypeomschrijving_url = 'http://example.com/omschrijving/1'
        data = {
            'zaaktype': f'http://testserver{zaaktype_url}',
            'omschrijving': 'illum',
            'resultaattypeomschrijving': resultaattypeomschrijving_url,
            'selectielijstklasse': 'https://garcia.org/',
            'archiefnominatie': 'blijvend_bewaren',
            'archiefactietermijn': 'P10Y',
            'brondatumArchiefprocedure': {
                'afleidingswijze': BrondatumArchiefprocedureAfleidingswijze.afgehandeld,
                'einddatumBekend': False,
                'procestermijn': 'P10Y',
                'datumkenmerk': '',
                'objecttype': '',
                'registratie': '',
            }
        }

        with requests_mock.Mocker() as m:
            m.register_uri('GET', resultaattypeomschrijving_url, json={
                'omschrijving': 'test'
            })
            response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        resultaattype = ResultaatType.objects.get()

        self.assertEqual(resultaattype.omschrijving_generiek, 'test')
        self.assertEqual(resultaattype.zaaktype, zaaktype)
        self.assertEqual(
            resultaattype.brondatum_archiefprocedure_afleidingswijze,
            BrondatumArchiefprocedureAfleidingswijze.afgehandeld
        )

    def test_delete_eigenschap(self):
        resultaattype = ResultaatTypeFactory.create()
        resultaattype_url = reverse('resultaattype-detail', kwargs={'uuid': resultaattype.uuid})

        response = self.client.delete(resultaattype_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResultaatType.objects.filter(id=resultaattype.id))

    def test_delete_eigenschap_fail_not_draft_zaaktype(self):
        resultaattype = ResultaatTypeFactory.create(zaaktype__draft=False)
        resultaattype_url = reverse('resultaattype-detail', kwargs={'uuid': resultaattype.uuid})

        response = self.client.delete(resultaattype_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-draft object is forbidden')
