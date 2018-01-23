from .factories import ZaakTypeFactory, StatusTypeFactory
from ztc.datamodel.choices import JaNee


class HaaglandenBaseTest(object):
    """
    Create instances for all models with realistic data.

    Use OD_Haaglanden_-Zaaktypecatalogus_v1.0-_20120210
    The case for 'Vergunningaanvraag regulier behandelen'(starting at page 95)
    """

    def setUp(self):
        #
        # kerngegevens
        #
        # TODO

        #
        # planning
        #
        # TODO

        #
        # Publicatie (van indiening)
        #
        # TODO

        #
        # kosten
        #
        # TODO

        #
        # Statusen
        #
        StatusTypeFactory.create(
            statustype_omschrijving='Intake afgerond',
            statustypevolgnummer=1,
            doorlooptijd_status=2,  # werkdagen
            informeren=JaNee.ja,
            toelichting='''
            Er wordt beoordeeld of de
            ontvangen aanvraag inderdaad in een reguliere
            procedure behandeld kan worden en of de
            aanvraag volledig is. Zo ja, dan wordt de zaak
            aangemaakt met daarbij de ontvangen
            documenten (aanvraag met bijlagen, opdracht tot
            behandeling van bevoegd gezag en eventueel
            ontvangstbevestiging) en wordt de
            zaakbehandelaar (medewerker of organisatie-
            onderdeel) bepaald (de startdatum is de datum
            van ontvangst door het bevoegd gezag, indien van
            toepassing). Als het bevoegd gezag de gemeente is,
            wordt zij geïnformeerd dat de intake heeft
            plaatsgevonden (d.m.v. een digitaal bericht). Als
            het bevoegd gezag de provincie is, wordt de
            ontvangstbevestiging aan de aanvrager gezonden,
            cc. naar provincie.
            Als de aanvraag niet in een reguliere procedure
            behandeld kan worden, wordt overgestapt naar
            een zaak van het type ‘Vergunningaanvraag
            uitgebreid behandelen’.''',
        # deze relatie is gedefinieerd op RolType en heeft de volgende regel:
        # roltypen = models.ManyToManyField('datamodel.RolType'
        # is_van = models.ForeignKey('datamodel.ZaakType
        )
        StatusTypeFactory.create(
            statustype_omschrijving='Getoetst op indieningsvereisten',
            statustypevolgnummer=2,
            doorlooptijd_status=4,  # werkdagen
            informeren=JaNee.ja,
            toelichting='''
            De aanvraag wordt beoordeeld
            op de kwaliteit (aanvaardbaarheid) van de
            ontvangen documenten. Als de aanvraag niet
            kwalitatief voldoende wordt bevonden, wordt de
            aanvrager om aanvullende gegevens verzocht. De
            procedure wordt dan tijdelijk opgeschort. Als de
            kwaliteit onvoldoende blijft, wordt deze buiten
            behandeling gesteld cq. niet-ontvankelijk
            verklaard. Ook kan de aanvraag niet-ontvankelijk
            worden verklaard als bijvoorbeeld de aanvrager
            niet gemachtigd is.
            Tijdens de toets kan alsnog blijken dat de aanvraag
            in een uitgebreide procedure behandeld moet
            worden. Daartoe wordt overgegaan naar een zaak
            van het type ‘Aanvraag vergunning uitgebreid
            behandelen’.
            ''',
        # deze relatie is gedefinieerd op RolType en heeft de volgende regel:
        # roltypen = models.ManyToManyField('datamodel.RolType'
        # is_van = models.ForeignKey('datamodel.ZaakType
        )

        #
        # rollen en betrokkenen
        #
        # TODO

