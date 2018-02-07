from django.test import TestCase
from django.urls import reverse

from ztc.datamodel.tests.base_tests import HaaglandenMixin
from ztc.datamodel.tests.factories import (
    FormulierFactory, ZaakTypeFactory, ZaakTypenRelatieFactory
)

from .base import ClientAPITestMixin


class ZaakTypeAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.zaaktype_list_url = reverse('api:zaaktype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
        })

    def test_get_list(self):
        response = self.api_client.get(self.zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_list_response(self):
        """
        Test the actual content of the response.
        """
        self.zaaktype2 = ZaakTypeFactory.create(
            datum_begin_geldigheid=self.zaaktype.datum_begin_geldigheid,
            maakt_deel_uit_van=self.catalogus,
        )
        self.zaaktype3 = ZaakTypeFactory.create(
            datum_begin_geldigheid=self.zaaktype.datum_begin_geldigheid,
            maakt_deel_uit_van=self.catalogus,
        )
        self.zaaktype4 = ZaakTypeFactory.create(
            datum_begin_geldigheid=self.zaaktype.datum_begin_geldigheid,
            maakt_deel_uit_van=self.catalogus,
        )
        # ghost zaaktype, not related to the one we test
        self.zaaktype5 = ZaakTypeFactory.create(
            datum_begin_geldigheid=self.zaaktype.datum_begin_geldigheid,
            maakt_deel_uit_van=self.catalogus,
        )

        for i in range(2):
            formulier = FormulierFactory.create(
                naam='formulier {}'.format(i),
                link='www.example.com'
            )
            self.zaaktype.formulier.add(formulier)

        # fill the ArrayFields
        self.zaaktype.trefwoord = ['trefwoord 1', 'trefwoord 2']
        self.zaaktype.verantwoordingsrelatie = ['verantwoordingsrelatie']

        # heeftGerelateerd..
        ZaakTypenRelatieFactory.create(
            zaaktype_van=self.zaaktype,
            zaaktype_naar=self.zaaktype2,
            aard_relatie='aard relatie',
        )
        # also create a relation between 4 and 5, to test that this one will not show up under self.zaaktype
        ZaakTypenRelatieFactory.create(
            zaaktype_van=self.zaaktype4,
            zaaktype_naar=self.zaaktype5,
        )

        self.zaaktype.is_deelzaaktype_van.add(self.zaaktype3)
        self.zaaktype.save()

        response = self.api_client.get(self.zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        results = json_response.pop('results')

        expected = {
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/'.format(self.catalogus.pk)
                }
            },
        }
        self.assertEqual(response.json(), expected)

        #
        # check results
        #
        self.assertEqual(len(results), 5)
        result = results[4]  # only check the last one (since we did the .save()), from haaglanden data

        heeftRelevantBesluittype = result.pop('heeftRelevantBesluittype')
        # it is http://testserver/api/v1/catalogussen/1/besluittypen/8/
        self.assertEqual(len(heeftRelevantBesluittype), 4)
        for besluittype in heeftRelevantBesluittype:
            self.assertTrue(besluittype.startswith('http://testserver/api/v1/catalogussen/{}/besluittypen/'.format(self.catalogus.pk)))

        expected_result = {
            'versiedatum': '',
            'maaktDeelUitVan': 'http://testserver/api/v1/catalogussen/{}/'.format(self.catalogus.pk),
            'omschrijving': 'Vergunningaanvraag regulier behandelen',
            'heeftGerelateerd': ['http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype2.pk)],  # TODO: check the through model ??
            'verlengingmogelijk': 'J',
            'doorlooptijd': 8,
            'aanleiding': 'De gemeente als bevoegd gezag heeft een aanvraag voor een\n                omgevingsvergunning of milieuwetgeving-gerelateerde vergunning\n                ontvangen.\n                De gemeente heeft geconstateerd dat het een enkelvoudige aanvraag\n                betreft met alleen een milieu-component of dat het een meervoudige\n                aanvraag betreft met betrekking tot een milieuvergunningplichtige\n                inrichting of -locatie en met een milieu-component (milieu-aspect is\n                ‘zwaartepunt’) .\n                De gemeente heeft de ODH gemandateerd om dergelijke aanvragen te\n                behandelen. Zij draagt de ODH op om de ontvangen aanvraag te\n                behandelen. De ODH heeft vastgesteld dat de aanvraag in een reguliere\n                procedure behandeld kan worden.\n                of:\n                De provincie als bevoegd gezag heeft een aanvraag voor een\n                omgevingsvergunning of milieuwetgevinggerelateerde vergunning\n      ',
            'indicatieInternOfExtern': '',
            'verantwoordingsrelatie': ['verantwoordingsrelatie'],
            'handelingInitiator': 'Aanvragen',
            'servicenorm': None,
            'handelingBehandelaar': '',
            'bronzaaktype': None,
            'identificatie': self.zaaktype.zaaktype_identificatie,
            'broncatalogus': None,
            'doel': 'Een besluit nemen op een aanvraag voor een vergunning, ontheffing of\n                vergelijkbare beschikking op basis van een gedegen beoordeling van die\n                aanvraag in een reguliere procedure.',
            'isDeelzaaktypeVan': ['http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype3.pk)],
            'omschrijvingGeneriek': None,
            'verlengingstermijn': 30,
            'archiefclassificatiecode': None,
            'vertrouwelijkheidAanduiding': 'OPENBAAR',
            'trefwoord': ['trefwoord 1', 'trefwoord 2'],
            'formulier': [
                {'link': 'www.example.com',
                 'naam': 'formulier 0'},
                {'link': 'www.example.com',
                 'naam': 'formulier 1'}],
            'referentieproces': {
                'naam': str(self.zaaktype.referentieproces),
                'link': None
            },
            'toelichting': 'Bij dit zaaktype draagt het bevoegd gezag de behandeling van de\n                vergunningaanvraag op aan de ODH. De start van de zaakbehandeling\n                verschilt naar gelang de aanvraag ontvangen is door de gemeente dan\n                wel de provincie als bevoegd gezag. Aangezien de gemeente de front-\n                office vormt (in het geval zij bevoegd gezag is), verzorgt zij haar deel van\n                de intake, met name registratie van de zaak en uitdoen van de ontvangst-\n                bevestiging. Daarna zet de ODH als back-office de behandeling voort. Als\n                de provincie het bevoegd gezag is, verzorgt de ODH het front-office en\n                voert de gehele intake uit, waaronder het uitdoen van de ontvangst-\n                bevestiging, en zet daarna als back-office de behandeling voort.\n                De ODH bepaalt tijdens haar intake, of zo spoedig mogelijk daarna, dat de\n                aanvraag in een reguliere procedure behandeld kan worden.',
            'verantwoordelijke': '', 'product_dienst': [{'naam': 'Vergunning voor milieu', 'link': None}],
            'publicatieIndicatie': 'J',
            'zaakcategorie': None,
            'opschortingAanhouding': 'J',
            'publicatietekst': 'N.t.b.',
            'onderwerp': 'Milieu-gerelateerde vergunning',
        }
        self.assertEqual(expected_result, result)

    def test_get_list_response_minimum_data(self):
        self.zaaktype.aanleiding = 'aanleiding'
        self.zaaktype.toelichting = 'toelichting'
        self.zaaktype.doel = 'doel'
        self.zaaktype.heeft_relevant_besluittype = []
        self.zaaktype.save()

        response = self.api_client.get(self.zaaktype_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'results': [
                {
                    'vertrouwelijkheidAanduiding': 'OPENBAAR',
                    'identificatie': self.zaaktype.zaaktype_identificatie,
                    'product_dienst': [{'naam': 'Vergunning voor milieu', 'link': None}],
                    'broncatalogus': None,
                    'publicatieIndicatie': 'J',
                    'trefwoord': [],
                    'zaakcategorie': None,
                    'toelichting': 'toelichting',
                    'handelingInitiator': 'Aanvragen',
                    'bronzaaktype': None,
                    'aanleiding': 'aanleiding',
                    'verlengingstermijn': 30,
                    'opschortingAanhouding': 'J',
                    'maaktDeelUitVan': 'http://testserver/api/v1/catalogussen/{}/'.format(self.zaaktype.maakt_deel_uit_van.pk),
                    'indicatieInternOfExtern': '',
                    'verlengingmogelijk': 'J',
                    'handelingBehandelaar': '',
                    'heeftGerelateerd': [],
                    'doel': 'doel',
                    'versiedatum': '',
                    'formulier': [],
                    'onderwerp': 'Milieu-gerelateerde vergunning',
                    'publicatietekst': 'N.t.b.',
                    'omschrijvingGeneriek': None,
                    'verantwoordingsrelatie': [],
                    'isDeelzaaktypeVan': [],
                    'servicenorm': None,
                    'archiefclassificatiecode': None,
                    'referentieproces': {'naam': str(self.zaaktype.referentieproces.naam), 'link': None},
                    'heeftRelevantBesluittype': [],
                    'doorlooptijd': 8,
                    'verantwoordelijke': '',
                    'omschrijving': 'Vergunningaanvraag regulier behandelen'
                }
            ],
            '_links': {
                'self': {'href': 'http://testserver/api/v1/catalogussen/3/zaaktypen/'}
            }
        }
        self.assertEqual(response.json(), expected)
