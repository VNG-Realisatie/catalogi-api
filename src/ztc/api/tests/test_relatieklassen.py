from unittest import skip

from rest_framework import status
from vng_api_common.tests import reverse, reverse_lazy

from ztc.datamodel.choices import RichtingChoices
from ztc.datamodel.models import ZaakInformatieobjectType
from ztc.datamodel.tests.factories import (
    InformatieObjectTypeFactory, ZaakInformatieobjectTypeArchiefregimeFactory,
    ZaakInformatieobjectTypeFactory, ZaakTypeFactory
)

from .base import APITestCase


class ZaakInformatieobjectTypeAPITests(APITestCase):
    maxDiff = None

    list_url = reverse_lazy(ZaakInformatieobjectType)

    def test_get_list_default_nonconcept(self):
        ziot1 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=True)
        ziot2 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=True)
        ziot3 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=False)
        ziot4 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=False)
        ziot4_url = reverse(ziot4)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{ziot4_url}')

    def test_get_detail(self):
        ztiot = ZaakInformatieobjectTypeFactory.create()
        url = reverse(ztiot)
        zaaktype_url = reverse(ztiot.zaaktype)
        informatie_object_type_url = reverse(
            ztiot.informatie_object_type,
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': f'http://testserver{url}',
            'zaaktype': f'http://testserver{zaaktype_url}',
            'informatieObjectType': f'http://testserver{informatie_object_type_url}',
            'volgnummer': ztiot.volgnummer,
            'richting': ztiot.richting,
            'statusType': None,
        }
        self.assertEqual(response.json(), expected)

    def test_create_ziot(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse(informatieobjecttype)
        data = {
            'zaaktype': f'http://testserver{zaaktype_url}',
            'informatieObjectType': f'http://testserver{informatieobjecttype_url}',
            'volgnummer': 13,
            'richting': RichtingChoices.inkomend,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ziot = ZaakInformatieobjectType.objects.get(volgnummer=13)

        self.assertEqual(ziot.zaaktype, zaaktype)
        self.assertEqual(ziot.informatie_object_type, informatieobjecttype)

    def test_create_ziot_fail_not_concept_zaaktype(self):
        zaaktype = ZaakTypeFactory.create(concept=False)
        zaaktype_url = reverse(zaaktype)
        informatieobjecttype = InformatieObjectTypeFactory.create()
        informatieobjecttype_url = reverse(informatieobjecttype)
        data = {
            'zaaktype': f'http://testserver{zaaktype_url}',
            'informatieObjectType': f'http://testserver{informatieobjecttype_url}',
            'volgnummer': 13,
            'richting': RichtingChoices.inkomend,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Creating relations between non-concept objects is forbidden')

    def test_create_ziot_fail_not_concept_informatieobjecttype(self):
        zaaktype = ZaakTypeFactory.create()
        zaaktype_url = reverse(zaaktype)
        informatieobjecttype = InformatieObjectTypeFactory.create(concept=False)
        informatieobjecttype_url = reverse(informatieobjecttype)
        data = {
            'zaaktype': f'http://testserver{zaaktype_url}',
            'informatieObjectType': f'http://testserver{informatieobjecttype_url}',
            'volgnummer': 13,
            'richting': RichtingChoices.inkomend,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Creating relations between non-concept objects is forbidden')

    def test_delete_ziot(self):
        ziot = ZaakInformatieobjectTypeFactory.create()
        ziot_url = reverse(ziot)

        response = self.client.delete(ziot_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ZaakInformatieobjectType.objects.filter(id=ziot.id))

    def test_delete_ziot_fail_not_concept_zaaktype(self):
        ziot = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False)
        ziot_url = reverse(ziot)

        response = self.client.delete(ziot_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-concept object is forbidden')

    def test_delete_ziot_fail_not_concept_informatieobjecttype(self):
        ziot = ZaakInformatieobjectTypeFactory.create(informatie_object_type__concept=False)
        ziot_url = reverse(ziot)

        response = self.client.delete(ziot_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = response.json()
        self.assertEqual(data['detail'], 'Deleting a non-concept object is forbidden')


class ZaakInformatieobjectTypeFilterAPITests(APITestCase):
    maxDiff = None
    list_url = reverse_lazy(ZaakInformatieobjectType)

    def test_filter_zaaktype(self):
        ztiot1, ztiot2 = ZaakInformatieobjectTypeFactory.create_batch(
            2,
            zaaktype__concept=False,
            informatie_object_type__concept=False
        )
        url = f'http://testserver{reverse(ztiot1)}'
        zaaktype1_url = reverse(ztiot1.zaaktype)
        zaaktype2_url = reverse(ztiot2.zaaktype)

        zaaktype1_url = f'http://testserver{zaaktype1_url}'
        zaaktype2_url = f'http://testserver{zaaktype2_url}'

        response = self.client.get(self.list_url, {'zaaktype': zaaktype1_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()[0]['url'], url)
        self.assertEqual(response.json()[0]['zaaktype'], zaaktype1_url)
        self.assertNotEqual(response.json()[0]['zaaktype'], zaaktype2_url)

    def test_filter_informatieobjecttype(self):
        ztiot1, ztiot2 = ZaakInformatieobjectTypeFactory.create_batch(
            2,
            zaaktype__concept=False,
            informatie_object_type__concept=False
        )
        url = f'http://testserver{reverse(ztiot1)}'
        informatie_object_type1_url = reverse(ztiot1.informatie_object_type)
        informatie_object_type2_url = reverse(ztiot2.informatie_object_type)

        informatie_object_type1_url = f'http://testserver{informatie_object_type1_url}'
        informatie_object_type2_url = f'http://testserver{informatie_object_type2_url}'

        response = self.client.get(self.list_url, {'informatieObjectType': informatie_object_type1_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['url'], url)
        self.assertEqual(response.json()[0]['informatieObjectType'], informatie_object_type1_url)
        self.assertNotEqual(response.json()[0]['informatieObjectType'], informatie_object_type2_url)

    def test_filter_ziot_publish_all(self):
        ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=True)
        ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=True)
        ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=False)
        ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=False)

        response = self.client.get(self.list_url, {'publish': 'all'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 4)

    def test_filter_ziot_publish_concept(self):
        ziot1 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=True)
        ziot2 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=True)
        ziot3 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=False)
        ziot4 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=False)
        ziot1_url = reverse(ziot1)

        response = self.client.get(self.list_url, {'publish': 'concept'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{ziot1_url}')

    def test_filter_ziot_publish_nonconcept(self):
        ziot1 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=True)
        ziot2 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=True)
        ziot3 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=True, informatie_object_type__concept=False)
        ziot4 = ZaakInformatieobjectTypeFactory.create(zaaktype__concept=False, informatie_object_type__concept=False)
        ziot4_url = reverse(ziot4)

        response = self.client.get(self.list_url, {'publish': 'nonconcept'})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['url'], f'http://testserver{ziot4_url}')


@skip("Not MVP yet")
class ZaakInformatieobjectTypeArchiefregimeAPITests(APITestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.ziot = ZaakInformatieobjectTypeFactory.create(
            zaaktype__catalogus=self.catalogus,
            informatie_object_type__catalogus=self.catalogus,
            informatie_object_type__zaaktypes=None,
            volgnummer=1,
        )

        self.informatieobjecttype = self.ziot.informatie_object_type
        self.zaaktype = self.ziot.zaaktype

        self.rstiotarc = ZaakInformatieobjectTypeArchiefregimeFactory.create(
            zaak_informatieobject_type=self.ziot,
            resultaattype__is_relevant_voor=self.zaaktype,
            resultaattype__bepaalt_afwijkend_archiefregime_van=None,
        )

        self.resultaattype = self.rstiotarc.resultaattype

        self.rstiotarc_list_url = reverse('api:rstiotarc-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })

        self.rstiotarc_detail_url = reverse('api:rstiotarc-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.rstiotarc.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.rstiotarc_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.rstiotarc_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver{}'.format(self.rstiotarc_detail_url),
            'gerelateerde': 'http://testserver{}'.format(
                reverse('api:informatieobjecttype-detail', args=[
                    self.API_VERSION, self.catalogus.pk, self.informatieobjecttype.pk])
            ),
            'rstzdt.archiefactietermijn': 7,
            'rstzdt.archiefnominatie': '',
            'rstzdt.selectielijstklasse': None,
        }
        self.assertEqual(response.json(), expected)
