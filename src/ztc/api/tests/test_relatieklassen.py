from unittest import skip

from django.urls import reverse

from ztc.datamodel.tests.factories import (
    ZaakInformatieobjectTypeArchiefregimeFactory,
    ZaakInformatieobjectTypeFactory
)

from .base import APITestCase


@skip("Not MVP yet")
class ZaakInformatieobjectTypeAPITests(APITestCase):
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

        self.zktiot_list_url = reverse('api:zktiot-list', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })

        self.zktiot_detail_url = reverse('api:zktiot-detail', kwargs={
            'version': self.API_VERSION,
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.ziot.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.zktiot_list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue('results' in data)
        self.assertEqual(len(data['results']), 1)

    def test_get_detail(self):
        response = self.api_client.get(self.zktiot_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver{}'.format(self.zktiot_detail_url),
            'zdt.volgnummer': 1,
            'zdt.richting': 'Inkomend',
            'gerelateerde': 'http://testserver{}'.format(
                reverse('api:informatieobjecttype-detail', args=[
                    self.API_VERSION, self.catalogus.pk, self.informatieobjecttype.pk]),
            )
        }
        self.assertEqual(response.json(), expected)


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
