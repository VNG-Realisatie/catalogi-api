from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time

from ztc.datamodel.tests.base_tests import HaaglandenMixin
from ztc.datamodel.tests.factories import ZaakInformatieobjectTypeFactory

from .base import ClientAPITestMixin


@freeze_time('2018-02-07')  # datum_begin_geldigheid will be 'today': 'V20180207'
class ResultaatTypeAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.list_url = reverse('api:resultaattype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })
        self.resultaattype_geweigerd_detail_url = reverse('api:resultaattype-detail', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk,
            'pk': self.resultaattype_geweigerd.pk,
        })

        self.ziot = ZaakInformatieobjectTypeFactory.create(
            status_type=self.status_type_inhoudelijk_behandeld,
            zaaktype=self.zaaktype,
            # informatie_object_type=self.  # let the factory create a new one
            volgnummer=1,
            richting='richting',
        )
        self.iot = self.ziot.informatie_object_type

        self.besluittype_aanhoudingsbesluit.is_resultaat_van.add(self.resultaattype_geweigerd)
        self.besluittype_aanhoudingsbesluit.save()

        self.resultaattype_geweigerd.heeft_voor_brondatum_archiefprocedure_relevante = self.eigenschap_beoogde_producten
        self.resultaattype_geweigerd.heeft_verplichte_ziot.add(self.ziot)
        self.resultaattype_geweigerd.heeft_verplichte_zot.add(self.zaakobjecttype_milieu)
        self.resultaattype_geweigerd.save()

    def test_get_list(self):
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        results = json_response.pop('results')

        # there are 5 results. only check the one with omschrijving 'Verleend'
        self.assertEqual(len(results), 5)
        result = None
        for _result in results:
            if _result.get('omschrijving') == 'Verleend':
                result = _result

        # there are 3 expected results for leidtTot
        leidtTot = result.pop('leidtTot')
        self.assertEqual(len(leidtTot), 3)
        for leidt_tot in leidtTot:
            self.assertTrue(leidt_tot.startswith(
                'http://testserver/api/v1/catalogussen/{}/besluittypen/'.format(self.catalogus.pk)
            ))

        expected_result = {
            'heeftVerplichteZaakobjecttype': [],
            'isRelevantVoor': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk
            ),
            'archiefactietermijn': 14,
            'selectielijstklasse': None,
            'omschrijvingGeneriek': '',
            'brondatumProcedure': 'eigenschap',
            'einddatumObject': None,
            'ingangsdatumObject': 'V20180207',
            'archiefnominatie': '',
            'omschrijving': 'Verleend',
            'toelichting': None,
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/resultaattypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.resultaattype_verleend.pk,
            )
        }
        self.assertEqual(result, expected_result)

        self.assertEqual(json_response, {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/resultaattypen/'.format(
                        self.catalogus.pk, self.zaaktype.pk
                    )
                }
            }
        })

    def test_get_detail(self):
        response = self.api_client.get(self.resultaattype_geweigerd_detail_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'archiefactietermijn': 14,
            'archiefnominatie': '',
            'brondatumProcedure': 'eigenschap',
            'einddatumObject': None,
            'heeftVerplichteZaakobjecttype': [
                'http://testserver/api/v1/catalogussen/{}/zaakobjecttypen/{}/'.format(
                    self.catalogus.pk, self.zaakobjecttype_milieu.pk)
            ],
            'ingangsdatumObject': 'V20180207',
            'isRelevantVoor': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk),
            'leidtTot': [
                'http://testserver/api/v1/catalogussen/{}/besluittypen/{}/'.format(
                    self.catalogus.pk, self.besluittype_aanhoudingsbesluit.pk)
            ],
            'omschrijving': 'Geweigerd',
            'omschrijvingGeneriek': '',
            'selectielijstklasse': None,
            'toelichting': None,
            'url': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/resultaattypen/{}/'.format(
                self.catalogus.pk, self.zaaktype.pk, self.resultaattype_geweigerd.pk),
            # 'heeftVerplichtDocumentype': [
            #     'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/heeft_relevant/{}/'.format(
            #         self.catalogus.pk, self.zaaktype.pk, self.ziot.pk)
            # ],
            # 'heeftVoorBrondatumArchiefprocedureRelevante':
            #     'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/eigenschappen/{}/'.format(
            #         self.catalogus.pk, self.zaaktype.pk, self.eigenschap_beoogde_producten.pk),

        }
        self.assertEqual(expected, response.json())
