from unittest import skip

from rest_framework import status
from zds_schema.tests import reverse, reverse_lazy

from ztc.datamodel.models import ZaakInformatieobjectType
from ztc.datamodel.tests.factories import (
    ZaakInformatieobjectTypeArchiefregimeFactory,
    ZaakInformatieobjectTypeFactory
)

from .base import APITestCase


class ZaakInformatieobjectTypeAPITests(APITestCase):
    maxDiff = None

    list_url = reverse_lazy(ZaakInformatieobjectType)

    def test_get_list(self):
        ZaakInformatieobjectTypeFactory.create_batch(3)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_detail(self):
        ztiot = ZaakInformatieobjectTypeFactory.create()
        url = reverse(ztiot)
        zaaktype_url = reverse(ztiot.zaaktype, kwargs={'catalogus_uuid': ztiot.zaaktype.catalogus.uuid})
        informatie_object_type_url = reverse(
            ztiot.informatie_object_type,
            kwargs={'catalogus_uuid': ztiot.informatie_object_type.catalogus.uuid}
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

    def test_filter_zaaktype(self):
        ztiot1, ztiot2 = ZaakInformatieobjectTypeFactory.create_batch(2)
        url = f'http://testserver{reverse(ztiot1)}'
        zaaktype1_url = reverse(ztiot1.zaaktype, kwargs={
            'catalogus_uuid': ztiot1.zaaktype.catalogus.uuid
        })
        zaaktype2_url = reverse(ztiot2.zaaktype, kwargs={
            'catalogus_uuid': ztiot2.zaaktype.catalogus.uuid
        })

        zaaktype1_url = f'http://testserver{zaaktype1_url}'
        zaaktype2_url = f'http://testserver{zaaktype2_url}'

        response = self.client.get(self.list_url, {'zaaktype': zaaktype1_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['url'], url)
        self.assertEqual(response.json()[0]['zaaktype'], zaaktype1_url)
        self.assertNotEqual(response.json()[0]['zaaktype'], zaaktype2_url)

    def test_filter_informatieobjecttype(self):
        ztiot1, ztiot2 = ZaakInformatieobjectTypeFactory.create_batch(2)
        url = f'http://testserver{reverse(ztiot1)}'
        informatie_object_type1_url = reverse(ztiot1.informatie_object_type, kwargs={
            'catalogus_uuid': ztiot1.informatie_object_type.catalogus.uuid
        })
        informatie_object_type2_url = reverse(ztiot2.informatie_object_type, kwargs={
            'catalogus_uuid': ztiot2.informatie_object_type.catalogus.uuid
        })

        informatie_object_type1_url = f'http://testserver{informatie_object_type1_url}'
        informatie_object_type2_url = f'http://testserver{informatie_object_type2_url}'

        response = self.client.get(self.list_url, {'informatieObjectType': informatie_object_type1_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['url'], url)
        self.assertEqual(response.json()[0]['informatieObjectType'], informatie_object_type1_url)
        self.assertNotEqual(response.json()[0]['informatieObjectType'], informatie_object_type2_url)


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
