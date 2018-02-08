from django.test import TestCase
from django.urls import reverse

from freezegun import freeze_time

from ztc.datamodel.tests.base_tests import HaaglandenMixin

from .base import ClientAPITestMixin

from ztc.datamodel.tests.factories import EigenschapFactory


@freeze_time('2018-02-07')  # datum_begin_geldigheid will be 'today': 'V20180207'
class StatusTypeAPITests(ClientAPITestMixin, HaaglandenMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.statustype_list_url = reverse('api:statustype-list', kwargs={
            'version': '1',
            'catalogus_pk': self.catalogus.pk,
            'zaaktype_pk': self.zaaktype.pk
        })

        # create an 'eigenschap' and attach it to StatusType 'besluit genomen'
        self.new_eigenschap = EigenschapFactory.create(
            eigenschapnaam='Eigenschap',
            toelichting='Eigenschap toelichting',
            is_van=self.zaaktype,
        )
        self.new_eigenschap.status_type = self.status_type_besluit_genomen
        self.new_eigenschap.save()

        # use Besluit genomen as status_type for ZOT milieu
        self.zaaktypeobject_milieu.status_type = self.status_type_besluit_genomen
        self.zaaktypeobject_milieu.save()

    def test_get_list(self):
        response = self.api_client.get(self.statustype_list_url)
        self.assertEqual(response.status_code, 200)

        expected = {
            'results': [
                {
                    'volgnummer': 1,
                    'omschrijving': 'Intake afgerond',
                    'einddatumObject': None,
                    'doorlooptijd': 2,
                    'informeren': 'J',
                    'omschrijvingGeneriek': None,
                    'ingangsdatumObject': 'V20180207',
                    'toelichting': 'Er wordt beoordeeld of de\n                ontvangen aanvraag inderdaad in een reguliere\n                procedure behandeld kan worden en of de\n                aanvraag volledig is. Zo ja, dan wordt de zaak\n                aangemaakt met daarbij de ontvangen\n                documenten (aanvraag met bijlagen, opdracht tot\n                behandeling van bevoegd gezag en eventueel\n                ontvangstbevestiging) en wordt de\n                zaakbehandelaar (medewerker of organisatie-\n                onderdeel) bepaald (de startdatum is de datum\n                van ontvangst door het bevoegd gezag, indien van\n                toepassing). Als het bevoegd gezag de gemeente is,\n                wordt zij geïnformeerd dat de intake heeft\n                plaatsgevonden (d.m.v. een digitaal bericht). Als\n                het bevoegd gezag de provincie is, wordt de\n                ontvangstbevestiging aan de aanvrager gezonden,\n                cc. naar provincie.\n                Als de aanvr',
                    'checklistitem': [],
                    'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype.pk),
                    'statustekst': None,
                    'heeftVerplichteEigenschap': [],
                    'heeftVerplichteZaakObjecttype': [],
                }, {
                    'volgnummer': 2,
                    'omschrijving': 'Getoetst op indieningsvereisten',
                    'einddatumObject': None,
                    'doorlooptijd': 4,
                    'informeren': 'J',
                    'omschrijvingGeneriek': None,
                    'ingangsdatumObject': 'V20180207',
                    'toelichting': 'De aanvraag wordt beoordeeld\n                op de kwaliteit (aanvaardbaarheid) van de\n                ontvangen documenten. Als de aanvraag niet\n                kwalitatief voldoende wordt bevonden, wordt de\n                aanvrager om aanvullende gegevens verzocht. De\n                procedure wordt dan tijdelijk opgeschort. Als de\n                kwaliteit onvoldoende blijft, wordt deze buiten\n                behandeling gesteld cq. niet-ontvankelijk\n                verklaard. Ook kan de aanvraag niet-ontvankelijk\n                worden verklaard als bijvoorbeeld de aanvrager\n                niet gemachtigd is.\n                Tijdens de toets kan alsnog blijken dat de aanvraag\n                in een uitgebreide procedure behandeld moet\n                worden. Daartoe wordt overgegaan naar een zaak\n                van het type ‘Aanvraag vergunning uitgebreid\n                behandelen’.',
                    'checklistitem': [],
                    'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype.pk),
                    'statustekst': None,
                    'heeftVerplichteEigenschap': [],
                    'heeftVerplichteZaakObjecttype': [],
                }, {
                    'volgnummer': 3,
                    'omschrijving': 'Inhoudelijk behandeld',
                    'einddatumObject': None,
                    'doorlooptijd': 21,
                    'informeren': 'J',
                    'omschrijvingGeneriek': None,
                    'ingangsdatumObject': 'V20180207',
                    'toelichting': 'De aanvraag wordt allereerst\n                beoordeeld op de relevante wetgeving en\n                informatie over de milieu-inrichting of -locatie.\n                Waar nodig wordt in- en/of extern om een\n                beoordeling (toetsing) gevraagd (bijvoorbeeld als\n                er sprake is van BRIKS-onderdelen of van milieu-\n                aspecten die binnen de provincie ondergebracht\n                zijn bij één RUD). Dat kan leiden tot in- en/of\n                externe deelzaken (‘Toetsing uitvoeren’). De status\n                is bereikt met een eenduidig advies over het al dan\n                niet verlenen van de vergunning.',
                    'checklistitem': [],
                    'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype.pk),
                    'statustekst': None,
                    'heeftVerplichteEigenschap': [],
                    'heeftVerplichteZaakObjecttype': [],
                }, {
                    'volgnummer': 4,
                    'omschrijving': 'Besluit genomen',
                    'einddatumObject': None,
                    'doorlooptijd': 2,
                    'informeren': 'N',
                    'omschrijvingGeneriek': None,
                    'ingangsdatumObject': 'V20180207',
                    'toelichting': 'Op basis van de aanvraag en het advies met betrekking tot de \n                vergunning wordt het definitieve besluit op- en vastgesteld.',
                    'checklistitem': [],
                    'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype.pk),
                    'statustekst': None,
                    'heeftVerplichteEigenschap': [
                        'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/eigenschappen/{}/'.format(self.catalogus.pk, self.zaaktype.pk, self.new_eigenschap.pk)
                    ],
                    'heeftVerplichteZaakObjecttype': [
                        'http://testserver/api/v1/catalogussen/{}/zaakobjecttypen/{}/'.format(self.catalogus.pk, self.zaaktypeobject_milieu.pk)
                    ],
                }, {
                    'volgnummer': 6,
                    'omschrijving': 'Producten geleverd',
                    'einddatumObject': None,
                    'doorlooptijd': 3,
                    'informeren': 'N',
                    'omschrijvingGeneriek': None,
                    'ingangsdatumObject': 'V20180207',
                    'toelichting': 'Het besluit wordt verzonden en gepubliceerd en het zaakdossier wordt afgesloten \n                en gearchiveerd (indien de provincie het bevoegd gezag is) dan wel ter archivering \n                overgedragen aan het bevoegd gezag (indien dat de gemeente is).',
                    'checklistitem': [],
                    'isVan': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/'.format(self.catalogus.pk, self.zaaktype.pk),
                    'statustekst': None,
                    'heeftVerplichteEigenschap': [],
                    'heeftVerplichteZaakObjecttype': [],
                }
            ],
            '_links': {
                'self': {
                    'href': 'http://testserver/api/v1/catalogussen/{}/zaaktypen/{}/statustypen/'.format(self.catalogus.pk, self.zaaktype.pk)
                }
            }
        }
        self.assertEqual(response.json(), expected)
