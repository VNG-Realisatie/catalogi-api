from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time

from ztc.datamodel.tests.base_tests import HaaglandenMixin
from ztc.datamodel.tests.factories import ZaakTypenRelatieFactory, ZaakTypeFactory

from .base import ClientAPITestMixin


@freeze_time('2018-02-07')  # datum_begin_geldigheid will be 'today': 'V20180207'
class RelatieklassenAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
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
                   'aard_relatie': 'aard relatie',
                   'toelichting': None,
                   'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/{}/'.format(self.catalogus.pk, self.zaaktype.pk, self.relatie_1.pk),
                   'zaaktype_naar': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype2.pk),
                   'zaaktype_van': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype.pk)
               }, {
                   'aard_relatie': '',
                   'toelichting': None,
                   'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/{}/'.format(self.catalogus.pk, self.relatie_2.zaaktype_van.pk, self.relatie_2.pk),
                   'zaaktype_naar': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.relatie_2.zaaktype_naar.pk),
                   'zaaktype_van': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.relatie_2.zaaktype_van.pk),
               }
           ]
        }
        self.assertEqual(response.json(), expected)

    def test_get_detail(self):
        response = self.api_client.get(self.zaaktyperelatie_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'aard_relatie': 'aard relatie',
            'toelichting': None,
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_gerelateerd/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.relatie_1.pk),
            'zaaktype_naar': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype2.pk),
            'zaaktype_van': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk)
        }
        self.assertEqual(response.json(), expected)
