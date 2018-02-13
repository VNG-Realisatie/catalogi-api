from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time

from ztc.datamodel.models import InformatieObjectType
from ztc.datamodel.tests.base_tests import HaaglandenMixin
from ztc.datamodel.tests.factories import (
    ZaakInformatieobjectTypeFactory, ZaakTypeFactory, ZaakTypenRelatieFactory
)

from .base import ClientAPITestMixin


@freeze_time('2018-02-07')  # datum_begin_geldigheid will be 'today': 'V20180207'
class ZaakTypeRelatieAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.zaaktyperelatie_list_url = reverse('api:zaaktypenrelatie-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })

        self.zaaktype2 = ZaakTypeFactory.create(
            datum_begin_geldigheid=self.zaaktype.datum_begin_geldigheid,
            maakt_deel_uit_van=self.catalogus,
        )

        # heeftGerelateerd..
        self.relatie_1 = ZaakTypenRelatieFactory.create(
            zaaktype_van=self.zaaktype,
            zaaktype_naar=self.zaaktype2,
            aard_relatie='aard relatie',
        )
        # also create a relation between 4 and 5, to test that this one will not show up under self.zaaktype
        self.relatie_2 = ZaakTypenRelatieFactory.create(
            zaaktype_van__maakt_deel_uit_van=self.catalogus,
            zaaktype_naar__maakt_deel_uit_van=self.catalogus,
            # zaaktype_van=self.zaaktype4,
            # zaaktype_naar=self.zaaktype5,
        )

        # self.zaaktype.is_deelzaaktype_van.add(self.zaaktype3)
        self.zaaktype.save()

        self.zaaktyperelatie_detail_url = reverse('api:zaaktypenrelatie-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.relatie_1.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.zaaktyperelatie_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/'.format(
                        self.catalogus.pk, self.zaaktype.pk)
                }
            },
            'results': [
               {
                   'aardRelatie': 'aard relatie',
                   'toelichting': None,
                   'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/{}/'.format(
                       self.catalogus.pk, self.zaaktype.pk, self.relatie_1.pk),
                   'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                       self.catalogus.pk, self.zaaktype2.pk),
               }, {
                   'aardRelatie': '',
                   'toelichting': None,
                   'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/{}/'.format(
                       self.catalogus.pk, self.relatie_2.zaaktype_van.pk, self.relatie_2.pk),
                   'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                       self.catalogus.pk, self.relatie_2.zaaktype_naar.pk),
               }
           ]
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail(self):
        response = self.api_client.get(self.zaaktyperelatie_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'aardRelatie': 'aard relatie',
            'toelichting': None,
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.relatie_1.pk),
            'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype2.pk),
        }
        self.assertEqual(response.json(), expected)


@freeze_time('2018-02-07')  # datum_begin_geldigheid will be 'today': 'V20180207'
class ZaakInformatieobjectTypeAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.iot = InformatieObjectType.objects.first()

        # Create a relation between StatusType inhoudelijk behandeld and self.zaaktype
        self.ziot = ZaakInformatieobjectTypeFactory.create(
            status_type=self.status_type_inhoudelijk_behandeld,
            zaaktype=self.zaaktype,
            informatie_object_type=self.iot,
            volgnummer=1,
            richting='richting',
        )

        self.list_url_zktiot = reverse('api:zktiot-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.list_url_iotzkt = reverse('api:iotzkt-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'informatieobjecttype_pk': self.iot.pk
        })

        self.detail_url_zktiot = reverse('api:zktiot-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.ziot.pk,
        })
        self.detail_url_iotzkt = reverse('api:iotzkt-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'informatieobjecttype_pk': self.iot.pk,
            'pk': self.ziot.pk,
        })

    def test_get_list_zktiot(self):
        response = self.api_client.get(self.list_url_zktiot)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_relevant/'.format(
                        self.catalogus.pk, self.zaaktype.pk)
                }
            },
            'results': [
                {'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_relevant/{}/'.format(
                    self.catalogus.pk, self.zaaktype.pk, self.ziot.pk),
                 'zdt.volgnummer': 1,
                 'zdt.richting': 'richting',
                 'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/'.format(
                     self.catalogus.pk, self.iot.pk),
                 }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_get_list_iotzkt(self):
        response = self.api_client.get(self.list_url_iotzkt)
        self.assertEqual(response.status_code, 200)

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/is_relevant_voor/'.format(
                        self.catalogus.pk, self.iot.pk)
                }
            },
            'results': [
                {'url': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/is_relevant_voor/{}/'.format(
                    self.catalogus.pk, self.iot.pk, self.ziot.pk),
                 'zdt.volgnummer': 1,
                 'zdt.richting': 'richting',
                 'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                     self.catalogus.pk, self.zaaktype.pk),
                 }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail_zktiot(self):
        response = self.api_client.get(self.detail_url_zktiot)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_relevant/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.ziot.pk),
            'zdt.volgnummer': 1,
            'zdt.richting': 'richting',
            'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/'.format(
                self.catalogus.pk, self.iot.pk),
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail_iotzkt(self):
        response = self.api_client.get(self.detail_url_iotzkt)
        self.assertEqual(response.status_code, 200)

        expected = {
            'url': 'http://testserver/api/v1/catalogussen/{}/informatieobjecttypen/{}/is_relevant_voor/{}/'.format(
                self.catalogus.pk, self.iot.pk, self.ziot.pk),
            'zdt.volgnummer': 1,
            'zdt.richting': 'richting',
            'gerelateerde': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk),
        }
        self.assertEqual(response.json(), expected)
